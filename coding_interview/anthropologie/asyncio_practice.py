import asyncio
import random


class Solution:
    def __init__(self):
        self.concurrent_limit = 3
        self.queue = asyncio.Queue()

    async def work(self, task_id: int):
        async with asyncio.Semaphore(self.concurrent_limit):
            while True:
                if self.queue.qsize() > 0:
                    work_item = await self.queue.get()
                    print(f"Task {task_id} start working on {work_item}")
                    await asyncio.sleep(random.randint(1, 3))
                    print(f"Task {task_id} completed {work_item}")
                else:
                    print(f"Task {task_id} is waiting for work")
                    await asyncio.sleep(1)

    async def run(self):
        worker_tasks = [asyncio.create_task(self.work(i)) for i in range(self.concurrent_limit)]

        total_tasks = 10
        while total_tasks > 0:
            task_id = random.randint(1, 100)
            await self.queue.put(task_id)
            print("--------------------------------")
            await asyncio.sleep(1)
            total_tasks -= 1

        await asyncio.gather(*worker_tasks)


class Solution2:
    def __init__(self):
        self.concurrent_limit = 3
        self.semaphore = asyncio.Semaphore(self.concurrent_limit)
        self.concurrency = 0

    async def work(self, work_item: int):
        worker_id = random.randint(1, 100)
        async with self.semaphore:
            self.concurrency += 1
            print(f"Worker {worker_id} is working on {work_item}, concurrency: {self.concurrency}")
            await asyncio.sleep(random.randint(3, 5))
            print(f"Worker {worker_id} completed {work_item}")
            self.concurrency -= 1

    async def run(self):
        tasks = []
        total_tasks = 10
        
        for _ in range(total_tasks):
            task_id = random.randint(1, 100)
            tasks.append(asyncio.create_task(self.work(task_id)))
            # await self.work(task_id)
            print("--------------------------------")
            await asyncio.sleep(1)

        print(f"finished assigning tasks")
        await asyncio.gather(*tasks)

s = Solution2()
asyncio.run(s.run())