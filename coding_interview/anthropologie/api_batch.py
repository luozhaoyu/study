from typing import Any, Callable
from typing import *
import time
import asyncio
import random

class RequestDeduplicator:
    """
    Attributes:
        status: {
            key: task
        }
    """
    def __init__(self):
        self.status = {}
    
    async def fetch(self, key: str, fetcher: Callable[[str], Any]) -> Any:
        """
        Fetch data for key. If another request for same key is in-flight,
        wait for that result instead of making duplicate request.
        
        Args:
            key: Request identifier
            fetcher: Async function to fetch data
        
        Returns:
            Result from fetcher (shared if deduplicated)
        """
        if key in self.status:  # someone is fetching that
            print("someone else is processing key right now")
            return await self.status[key]
        
        # mark this is being processed
        self.status[key] = asyncio.create_task(fetcher(key))
        result = await self.status[key]
        return result
        

class BatchingClient:
    """
    1. accumulate fetch request via public interface fetch()
    2. when reach batch_size or max_wait_ms reaches, start to batch request
    
    Attributes:
        last_batch_time:
        batch_keys: [], current keys in the batch
    """
    def __init__(self, 
                 batch_size: int = 10,
                 max_wait_ms: int = 100):
        """
        Args:
            batch_size: Maximum items per batch
            max_wait_ms: Maximum time to wait before sending batch
        """
        self.last_batch_time = time.time()
        self.batch_keys = []
        self.batch_size = batch_size
        self.max_wait_ms = max_wait_ms
        self.batch_result = {}
        self.batch_ready_event = {}
        self.downstream_error_counter = 0
        
    def continue_batch(self) -> bool:
        """whether it should continue batch or no"""
        current_time = time.time()
        if (current_time - self.last_batch_time) * 1000 > self.max_wait_ms:
            return False
        if len(self.batch_keys) >= self.batch_size:
            return False
        return True
            
    
    async def fetch(self, key: str) -> Any:
        """
        Fetch data for key. Automatically batches requests.
        
        1. should_batch()?
        2. if yes, keep accumulating
            if no, send batch request
        """
        self.save_batch_key(key)
        self.batch_ready_event[key] = asyncio.Event()
        
        if self.continue_batch():  # should continue 
            await self.batch_ready_event[key].wait()
        else:
            # self.batch_result = await self._batch_fetcher(self.batch_keys)
            self.batch_result = await self._batch_fetcher_with_retry(self.batch_keys)
        # print(self.batch_result, key)
        return self.batch_result[key]
    
    def save_batch_key(self, key):
        self.batch_keys.append(key)
    
    async def is_result_ready(self) -> bool:
        """wait until batch result is ready"""
        await self.batch_ready_event.wait()
        
    async def wait_until_batch_timeout(self):
        """wait until next batch timeout"""
        elapsed = (time.time() - self.last_batch_time)
        if elapsed < self.max_wait_ms * 1000:  # need to wait longer
            await asyncio.sleep(0)
            
    def break_circuit_for_downstream(self):
        if self.downstream_error_counter > 3:
            return True
        return False
            
    async def _batch_fetcher_with_retry(self, keys: List[str]) -> Dict[str, Any]:
        sleep_seconds = 1
        retry = 0
        while retry < 3:
            retry += 1
            try:
                error_probability = random.random()
                if error_probability > 0.8:
                    raise Exception("Intention random error")
                return await self._batch_fetcher(keys)
            except Exception as e:
                last_exception = e
                print("downstream error")
                self.downstream_error_counter += 1
                await asyncio.sleep(sleep_seconds + 2 ** retry)
        raise last_exception
        
    async def _batch_fetcher(self, keys: List[str]) -> Dict[str, Any]:
        """Override this to implement actual batch API call."""
        # await self.wait_until_batch_timeout()
        print(f"batch fetching keys: {keys}")
        self.batch_keys = []
        await asyncio.sleep(2)

        for key in keys:
            try:
                self.batch_result[key] = f"{key}_fetched"
                error_probability = random.random()
                if error_probability > 0.5:
                    raise Exception("Intention random error")
                # print(self.batch_ready_event, key)
            except Exception as e:
                self.downstream_error_counter += 1
                print(f"{key} encountered error: {e}")
                self.batch_result[key] = f"{key}_error"
            finally:
                self.batch_ready_event[key].set()
        # update
        self.last_batch_time = time.time()
        self.batch_keys = []
        return self.batch_result


class CachedBatchingClient(BatchingClient):
    """
    Attributes:
        cache: {
            key: {
                "value": actual value
                "expire": expire time
            }
        }
    """
    def __init__(self, 
                 batch_size: int = 10,
                 max_wait_ms: int = 100,
                 cache_ttl_seconds: int = 300):
        """Add LRU cache with TTL to batching client."""
        super().__init__(batch_size, max_wait_ms)
        self.cache = {}
        self.cache_ttl_seconds = cache_ttl_seconds
        
    def save_to_cache(self, key: str, value):
        current_time = time.time()
        self.cache[key] = {
            "value": value,
            "expire": current_time + self.cache_ttl_seconds,
        }
    
    async def fetch(self, key: str, bypass_cache: bool = False) -> Any:
        """Fetch with automatic caching."""
        current_time = time.time()
        if bypass_cache or key not in self.cache:  # bypass or not cached
            result = await super().fetch(key)
            self.save_to_cache(key, result)
            return result
        
        # cache exists
        # check cache not expire
        if current_time <= self.cache[key]["expire"]:
            print("cache is still valid")
            return self.cache[key]["value"]
            
        # expired
        result = await super().fetch(key)
        self.save_to_cache(key, result)
        return result
        
        
async def test():
    dedup = RequestDeduplicator()

    async def slow_fetch(key):
        await asyncio.sleep(1)  # Simulate slow API
        return f"data_{key}"

    # Make 5 concurrent requests for same key
    results = await asyncio.gather(
        dedup.fetch("user123", slow_fetch),
        dedup.fetch("user123", slow_fetch),
        dedup.fetch("user123", slow_fetch),
        dedup.fetch("user123", slow_fetch),
        dedup.fetch("user123", slow_fetch),
    )
    print(results)
    
    
async def test2():
    # Example 2: Batching
    client = BatchingClient(batch_size=2, max_wait_ms=2000)

    # Make 25 requests within 50ms
    tasks = [client.fetch(f"key_{i}") for i in range(6)]
    results = await asyncio.gather(*tasks)
    
    print(results)
    

async def test3():
    client = CachedBatchingClient(batch_size=2, max_wait_ms=2000)

    tasks = [client.fetch(f"key_{i}") for i in range(6)]
    tasks2 = [client.fetch(f"key_{i}") for i in range(6)]
    results = await asyncio.gather(*tasks)
    print(results)
    results = await asyncio.gather(*tasks2)
    print(results)
    

asyncio.run(test3())