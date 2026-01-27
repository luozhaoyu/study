"""
11:22
11:55 passed test
"""
import asyncio
from copyreg import pickle
from dataclasses import dataclass
import time
import datetime
import pickle

@dataclass
class Item:
    pass

class LRUCache:
    """
    Track serialization metadata (size of each value when serialized)
    The cache should maintain LRU order across persist/load cycles and provide accurate memory usage based on serialized sizes.

    LRU datastructure:
        dict + list by order

    - concurrency support
    - O(1) get/put -> OrderedDict or double-linked list
    - background persistence -> begin a transaction, includes all new changes, upon finish persistence, apply(persist) all new changes
    - load latest 10k items to warm up
    - 

    Attributes:
        storage: dict {
            key1: item1
        }
        ordered_list: [item1, value2, value3] -> t0, t1, t2 -> t0 oldest
        item1 = (timestamp, key, value)
        size_metadata: dict {
            key: item_size
        }
    """
    def __init__(self, capacity=3):
        self.storage = {}
        self.ordered_list = []
        self.size_metadata = {}
        self.capacity = 3

    def get(self, key):
        """
        1. get if exists
        2. update item to be latest
        """
        if key not in self.storage:
            return None

        # update item
        self.storage[key][0] = time.time()
        self.ordered_list.sort()

        return self.storage[key][2]
    
    def put(self, key, value):
        """
        1. update item
        2. update item to be latest
        """
        if key in self.storage:
            item = self.storage[key]
            item[0] = time.time()
            # keep thing in sort
            self.ordered_list.sort()
            return item[2]

        # insert a new one
        item = [time.time(), key, value]
        self.storage[key] = item
        self.ordered_list.append(item)

        # evict if over capacity
        self.keep_within_capacity()

    def keep_within_capacity(self):
        while len(self.storage) > self.capacity:
            # find the oldest one
            oldest_item = self.ordered_list.pop(0)
            key = oldest_item[1]
            del self.storage[key]
            print("evict one item")

    def persist(self) -> str:
        output_filepath = f"persist_data_{datetime.datetime.now()}"
        whole_obj = {
            "capacity": self.capacity,
            "storage": self.storage,
            "ordered_list": self.ordered_list,
            "size_metadata": self.size_metadata,
        }
        print(whole_obj)
        with open(output_filepath, 'wb') as f:
            pickle.dump(whole_obj, f)
        return output_filepath

    def load(self, filepath:str):
        with open(filepath, 'rb') as f:
            whole_obj = pickle.load(f)
            self.capacity = whole_obj["capacity"]
            self.storage = whole_obj["storage"]
            self.ordered_list = whole_obj["ordered_list"]
            self.size_metadata = whole_obj["size_metadata"]


import aiofiles
class ConcurrentLRUCache(LRUCache):
    def __init__(self, capacity=3):
        super().__init__(capacity)
        self.lock = asyncio.Lock()

    # async def get(self, key):
    #     async with self.lock:
    #         return super().get(key)

    # async def put(self, key, value):
    #     async with self.lock:
    #         return super().put(key, value)
    async def persist(self) -> str:
        output_filepath = f"persist_data_{datetime.datetime.now()}"
        whole_obj = {
            "capacity": self.capacity,
            "storage": self.storage,
            "ordered_list": self.ordered_list,
            "size_metadata": self.size_metadata,
        }
        data = pickle.dumps(whole_obj)
        async with aiofiles.open(output_filepath, 'wb') as f:
            await f.write(data)
        return output_filepath


def assert_equal(a, b):
    if a != b:
        raise Exception(f"not equal: {a} != {b}")


def test1():
    cache = LRUCache(capacity=3)
    cache.put("key1", {"data": "large_object", "size": 1000})
    cache.put("key2", [1, 2, 3, 4, 5])
    cache.put("key3", "simple_string")
    cache.get("key1")  # Makes key1 most recent
    cache.put("key5", "new thing")
    filepath = cache.persist()
    # Simulates restart
    new_cache = LRUCache(capacity=3)
    new_cache.load(filepath)
    # LRU order preserved: key1 (most recent), key3, key2
    new_cache.put("key4", "new")
    assert_equal(new_cache.get("key2"), None)
    assert_equal(new_cache.get("key3"), None)
    # Should evict key2 (least recent)
    print("passed test1")

def test2():
    cache = LRUCache(capacity=100)
    # Load with 100 items
    cache.persist()
    # File size should be proportional to serialized content
    print("passed test2")

test1()
test2()