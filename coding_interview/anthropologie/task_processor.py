from typing import Callable, List, Any, Dict
import multiprocessing
from multiprocessing import Pool

from dataclasses import dataclass
from typing import Optional
import time
import random

@dataclass
class TaskResult:
    task_id: int
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration_seconds: float = 0.0


class TaskProcessor:
    def __init__(self, num_workers: int = 4):
        """
        Args:
            num_workers: Number of worker processes
        """
        self.num_workers = num_workers
        self.pool = None
        self.task_queue = multiprocessing.Queue()
        self.task_func = None
        self.result_queue = multiprocessing.Queue()
    
    def process_tasks(self, 
                     tasks: List[Any], 
                     task_func: Callable[[Any], Any]) -> List[Any]:
        """
        Process tasks in parallel using worker pool.
        
        Args:
            tasks: List of task inputs
            task_func: Function to apply to each task
        
        Returns:
            List of results in same order as input tasks
        """
        self.task_func = task_func
        for index, task in enumerate(tasks):
            self.task_queue.put((index, task))
        print(f"task queue: {self.task_queue.qsize()}")
        self.pool = Pool(self.num_workers)
        results = self.pool.map(task_func, tasks)
        return results
        
    def worker_main(self):
        print("started")
        while self.task_queue:
            index, task = self.task_queue.get()
            result = self.task_func(task)
            self.result_queue.append((index, result))
    
    def shutdown(self) -> None:
        """Clean up resources."""
        self.pool.close()
        self.pool.join()

    def process_with_progress(self,
                            tasks: List[Any],
                            task_func: Callable[[Any], Any],
                            timeout_seconds: Optional[float] = None,
                            progress_callback: Optional[Callable[[int, int], None]] = None
                            ) -> List[TaskResult]:
        """
        Process tasks with progress tracking and timeout.
        
        Args:
            tasks: List of task inputs
            task_func: Function to apply to each task
            timeout_seconds: Optional timeout per task
            progress_callback: Called with (completed, total) after each task
        
        Returns:
            List of TaskResult objects
        """
        total = len(tasks)
        completed = 0
            
        self.pool = multiprocessing.Pool(self.num_workers)
        iter = self.pool.imap_unordered(task_func, tasks)
        try:
            while completed < total:
                result = iter.next(timeout_seconds)
                print(result)
                completed += 1
        finally:
            progress_callback(completed, total)


    def process_with_retry(self,
                          tasks: List[Any],
                          task_func: Callable[[Any], Any],
                          max_retries: int = 3,
                          retry_delay_seconds: float = 1.0,
                          timeout_seconds: Optional[float] = None
                          ) -> Dict[str, Any]:
        """
        Process tasks with automatic retry on failure.
        
        Args:
            tasks: List of task inputs
            task_func: Function to apply to each task
            max_retries: Maximum retry attempts per task
            retry_delay_seconds: Delay between retries
            timeout_seconds: Optional timeout per task (total time including retries)
        
        Returns:
            {
                "successful": List[TaskResult],    # Successfully completed
                "failed": List[TaskResult],         # Failed after all retries
                "total_time": float,                # Total processing time
                "success_rate": float               # Percentage successful
            }
        """
        start_time = time.time()
        
        with multiprocessing.Manager() as manager:
            result_queue = manager.Queue()
            
            with Pool(self.num_workers) as pool:
                async_results = []
                for index, task in enumerate(tasks):
                    ar = pool.apply_async(
                        worker_with_retry_main, 
                        args=(task_func, task, max_retries, retry_delay_seconds, timeout_seconds, index, result_queue)
                    )
                    async_results.append(ar)
                
                # Wait for all tasks to complete (more efficient than sleeping)
                for ar in async_results:
                    ar.wait()  # Wait for each async result to finish
            
            # Collect all results from queue
            all_results = []
            while not result_queue.empty():
                result = result_queue.get()
                all_results.append(result)
        
        # Categorize results
        successful = [r for r in all_results if r.success]
        failed = [r for r in all_results if not r.success]
        total_time = time.time() - start_time
        success_rate = (len(successful) / len(tasks) * 100) if tasks else 0
        
        return {
            "successful": successful,
            "failed": failed,
            "total_time": total_time,
            "success_rate": success_rate
        }
            
        
def worker_with_retry_main(task_func, task, max_retries, retry_delay_seconds, timeout_seconds, task_id, result_queue) -> TaskResult:
    """Worker function that executes a task with retry logic."""
    retry = 0
    start_time = time.time()
    tr: TaskResult = TaskResult(task_id, True)
    last_error = None
    
    while retry < max_retries:
        # Check if we've exceeded the total timeout
        if timeout_seconds and (time.time() - start_time) >= timeout_seconds:
            tr.success = False
            tr.error = f"Timeout after {timeout_seconds}s (completed {retry} attempts)"
            break
            
        try:
            retry += 1
            result = task_func(task)
            
            # Success!
            tr.result = result
            tr.success = True
            tr.error = None
            break
            
        except Exception as e:
            last_error = str(e)
            tr.success = False
            tr.error = last_error
            
            if retry < max_retries:
                # Check if we have time for another retry
                if timeout_seconds and (time.time() - start_time + retry_delay_seconds) >= timeout_seconds:
                    tr.error = f"Timeout during retry {retry}/{max_retries}. Last error: {last_error}"
                    break
                    
                time.sleep(retry_delay_seconds)
                continue
            else:
                # Exceeded max retries
                tr.error = f"Failed after {max_retries} attempts. Last error: {last_error}"
                break
    
    tr.duration_seconds = time.time() - start_time
    result_queue.put(tr)
    return tr
            
        
def expensive_computation(n: int) -> int:
    """Simulate CPU-intensive work"""
    return sum(i * i for i in range(n))
    
def test():
    tp = TaskProcessor()
    print(tp.process_tasks([1, 2, 3, 4, 5], expensive_computation))
    tp.shutdown()


def slow_task(x: int) -> int:
    time.sleep(1)
    return x * 2

def on_progress(completed: int, total: int):
    print(f"Progress: {completed}/{total}")
    
def flaky_task(x: int) -> int:
    """Fails 50% of the time"""
    if random.random() < 0.5:
        raise ValueError("Random failure")
    return x * 2
  
def test2():
    processor = TaskProcessor(num_workers=4)
    results = processor.process_with_progress(
        tasks=list(range(10)),
        task_func=slow_task,
        timeout_seconds=2.0,
        progress_callback=on_progress
    )
    
def test3():
    """Test retry mechanism with flaky tasks"""
    print("\n=== Test: Retry mechanism with flaky tasks ===")
    processor = TaskProcessor(num_workers=4)
    result = processor.process_with_retry(
        tasks=list(range(20)),
        task_func=flaky_task,
        max_retries=3,
        retry_delay_seconds=0.5,
        timeout_seconds=5,  # 5 seconds total per task
    )
    
    print(f"\n📊 Summary:")
    print(f"  Total tasks: {len(result['successful']) + len(result['failed'])}")
    print(f"  Successful: {len(result['successful'])}")
    print(f"  Failed: {len(result['failed'])}")
    print(f"  Success rate: {result['success_rate']:.1f}%")
    print(f"  Total time: {result['total_time']:.2f}s")
    
    if result['failed']:
        print(f"\n❌ Failed tasks:")
        for tr in result['failed']:
            print(f"  Task {tr.task_id}: {tr.error} (took {tr.duration_seconds:.2f}s)")
    
    if result['successful']:
        print(f"\n✅ Sample successful tasks:")
        for tr in result['successful'][:5]:  # Show first 5
            print(f"  Task {tr.task_id}: result={tr.result} (took {tr.duration_seconds:.2f}s)")

if __name__ == "__main__":        
    test3()