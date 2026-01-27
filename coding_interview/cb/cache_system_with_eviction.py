"""
# Exercise 4: Cache System with Eviction
*Tests your understanding of LRU/LFU policies and time-based operations.*

### Level 1: Simple Key-Value Store with Capacity
Implement a cache with maximum capacity.
- **Operations:** `["PUT", "key", "value"]`, `["GET", "key"]`
- **Logic:**
  - Cache has a maximum capacity (e.g., 3 items)
  - When full and adding a new key, evict the **oldest inserted** key (FIFO)
- **Return:** For GET, return the value or `null`. For PUT, return `"stored"` or `"evicted:old_key"`

### Level 2: LRU (Least Recently Used) Policy
Change eviction to LRU instead of FIFO.
- **Logic:**
  - Every GET or PUT updates the "last accessed" time
  - When evicting, remove the key that was accessed longest ago
  - **Hint:** You need a Hash Map for O(1) lookup AND a way to track access order (Doubly Linked List or OrderedDict in Python)
- **New Operation:** `["STATS"]` returns the current cache size and the LRU key

### Level 3: TTL (Time-To-Live) + Priority Levels
Add expiration and priority-based eviction.
- **New Format:** `["PUT", "key", "value", "ttl", "priority"]`
  - `ttl`: seconds until expiration (0 = no expiration)
  - `priority`: integer (higher = more important)
- **Logic:**
  - GET on an expired key returns `null` and removes it from cache
  - When evicting, prefer expired keys first, then lowest priority, then LRU
  - Add `["CLEAN"]` operation that removes all expired entries
- **New Operation:** `["GET_AT", "key", "timestamp"]` to check value at a specific time

### Level 4: Distributed Cache Consistency
Simulate a 3-node distributed cache system.
- **New Format:** Operations now include node ID: `["PUT", "node_1", "key", "value"]`
- **Logic:**
  - Data should replicate to at least 2 nodes
  - `["GET", "any_node", "key"]` should return the value if it exists on ANY node
  - Add `["SYNC", "from_node", "to_node"]` to manually synchronize caches
  - Handle conflicts: if the same key exists with different values on different nodes, the one with the latest timestamp wins
- **New Operations:**
  - `["GET_REPLICATION_STATUS", "key"]` returns list of nodes containing this key
  - `["FAILOVER", "failed_node"]` redistributes that node's data to remaining nodes
- **Challenge:** Track which keys are on which nodes efficiently (nested hash maps)
"""


import time
import random
import bisect
from typing import List, Tuple, Dict

class Item():
    """
    item can form linked list that has prev and next item
    Attributes:
        timestamp: recent update
        ttl: time to live until this time
        snapshot: [], a list recording the change
    """
    def __init__(self, key, value, timestamp=None, ttl=0, priority=None):
        self.prev = None
        self.next = None
        self.key = key
        self.value = value
        self.timestamp = timestamp
        self.set_ttl(ttl)
        self.priority = priority

    def set_ttl(self, ttl):
        if ttl == 0:
            self.ttl = 0
            return
        self.ttl = ttl + time.time()

    def __str__(self):
        return f"{(self.key, self.value, self.timestamp)}"

    def __repr__(self):
        return str(self)

    def put(self, value):
        self.value = value
        self.snapshot.append((value, time.time()))

    def get_at(self, timestamp):
        """
        1. find the right most item that is <= timestamp in snapshot
        2. return that
        """
        index = bisect.bisect_left(self.snapshot, timestamp, key=lambda snapshot:snapshot[1])
        if index >= 0:
            return self.snapshot[index][0]


class Cache:
    def __init__(self, capacity=3):
        """
        evicting item needs refresh item to the latest place
        linkedList: head is latest, tail is oldest
        
        enforce_capacity: evict expires first, then check (priority, timestamp)

        Attributes:
            storage: { key: Item}, use OrderedDict to enforce 
            ttl_list: a list to order item by ttl 
            replica: [], list of replica for replication
        """
        self.capacity = capacity
        self.storage: Dict[str, Item] = {}
        self.ttl_list: List[Item] = []
        self.head = Item(None, None)
        self.tail = Item(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.replica = []

    def evict(self):
        """pop out the oldest key

        1. pop the key
            self.tail.prev is always the oldest key
            new_prev -> prev -> tail
        2. pop from the ttl list
        """
        if self.tail.prev == self.head:  # it means empty
            return "evicted:null"

        key_to_be_evicted = self.tail.prev.key
        return self._evict_from_linked_list_and_storage(key_to_be_evicted)

    def _evict(self, key):
        """evict a specific key
        1. remove from ttl_list
        2. remove from link list
        """
        index = 0
        while index < len(self.ttl_list):
            element = self.ttl_list[index]
            if element.key == key:
                self.ttl_list.pop(index)
                break
            index += 1
        
        self._evict_from_linked_list_and_storage(key)

    def _evict_from_linked_list_and_storage(self, key):
        item = self.storage[key]

        # connect prev and next
        prev = item.prev
        next = item.next
        prev.next = next
        next.prev = prev
       
        # evict the key, and from storage
        del self.storage[key]
        return f"evicted:{key}"

    def refresh_existing(self, key):
        """update key timestamp, then move it to the latest position
        prev -> now -> next
        1. connect the current position
        2. move to head
        """
        item = self.storage[key]
        item.timestamp = time.time()
        # step 1
        prev_item = item.prev
        next_item = item.next
        prev_item.next = next_item
        next_item.prev = prev_item

        # step 2
        self.insert_to_head(item)

    def insert_to_head(self, item):
        new_next = self.head.next
        new_next.prev = item
        item.next = new_next

        self.head.next = item
        item.prev = self.head

    def insert_to_ttl_list(self, item):
        """insert into ordered list
        1. since ttl is ordered, find the best index for insertion
        2. insert
        """
        return bisect.insort(self.ttl_list, item, key=lambda i:i.ttl)

    def _insert(self, item):
        """insert an item to cache
        1. update the linkedList
        2. update the ttl list
        """
        self.insert_to_head(item)
        if item.ttl > 0:  # only item would expire need to add into ttl_list
            self.insert_to_ttl_list(item)

    def get(self, operation):
        if len(operation) < 2:
            print("error")
            return "error"

        _, key = operation
        if key not in self.storage:
            return "null"

        self.refresh_existing(key)
        return self.storage[key].value

    def fetch(self, key):
        """fetch would just return without updating the key
        """
        return self.storage[key]

    def put(self, operation):
        if len(operation) < 3:
            print("error")
            return "error"

        key = None
        value = None
        ttl = 0
        priority = None

        if len(operation) == 3:
            _, key, value = operation
        if len(operation) == 5:
            _, key, value, ttl, priority = operation

        self.replicate_put(operation)

        if key not in self.storage:
            self.storage[key] = Item(key, value, time.time(), ttl, priority)
            self._insert(self.storage[key])
            if len(self.storage) > self.capacity:
                return self._keep_within_capacity()
        else:
            self.storage[key].value = value
            self.refresh(key)

        return "stored"

    def stats(self):
        return len(self.storage), self.storage.keys()

    def _keep_within_capacity(self):
        """ensure the storage is within capacity
        """
        if len(self.storage) > self.capacity:
            print(f"warning: out of capacity, capacity: {len(self.storage)}, cleaning ...")
            self.clean()

        key = None
        # still has too many items
        while len(self.storage) > self.capacity:
            key = self._find_key_to_evict()
            print(f"warning: out of capacity, capacity: {len(self.storage)}, force evicting {key}")
            self._evict(key)
        return f"evicted:{key}"

    def _find_key_to_evict(self):
        """find next key for eviction
        1. check expired key first
        2. check (is_expired, priority, timestamp)
        """
        if not self.storage:
            print("cache is empty, no key for eviction!")
            return

        key_to_evict = next(iter(self.storage.keys()))  # init with the first key
        current_priority = self.storage[key_to_evict].priority
        current_timestamp = self.storage[key_to_evict].timestamp
        for key, item in self.storage.items():
            if item.ttl != 0 and item.ttl < time.time():  # expired
                return key

            if item.priority and current_priority and item.priority > current_priority:  # lower priority
                current_priority = item.priority
                key_to_evict = key
                current_timestamp = item.timestamp
            if item.priority == current_priority and item.timestamp < current_timestamp:  # same priority but older timestamp
                current_priority = item.priority
                key_to_evict = key
                current_timestamp = item.timestamp
            # print(current_priority, current_timestamp, key, item, key_to_evict)

        # print(f"evicting {key_to_evict} from: {self.storage}")
        return key_to_evict

    def clean(self):
        """checking the oldest key until expiration
        1. go through ttl_list one by one
        2. check each other
        """
        while self.ttl_list:
            element = self.ttl_list[0]
            if element.ttl < time.time():  # now passed ttl
                key = element.key
                self._evict_from_linked_list_and_storage(key)
                # remove from ttl_list
                self.ttl_list.pop(0)
            else:  # not passing, we finished cleaning
                return

    def get_at(self, key, timestamp):
        if key not in self.storage:
            return "null"
        return self.storage[key].get_at(timestamp)

    def apply(self, operation):
        action = operation[0]
        if action == "PUT":
            return self.put(operation)
        elif action == "GET":
            return self.get(operation)
        elif action == "STATS":
            return self.stats()
        elif action == "CLEAN":
            return self.clean()
        elif action == "GET_AT":
            return self.get_at(operation[1], operation[2])

    def add_replica(self, replica):
        return self.replica.append(replica)

    def replicate_put(self, operation):
        """replicate put operation to other nodes
        1. find all other nodes
        2. each node applies this operation
        """
        for node in self.replicas:
            node.put(operation)

    def has(self, key):
        return key in self.storage


class Cluster:
    def __init__(self, num_nodes=3):
        """
        init num_nodes caches

        each node should find at least 2 other nodes as replica
        """
        self.nodes: Dict[str, Cache] = {}

        for i in range(num_nodes):
            node_name = f"node_{i}"
            self.nodes[node_name] = Cache()

        all_nodes = self.nodes.values()
        # add replica
        for primary in self.nodes.values():
            replica_list = random.sample(all_nodes, 2)
            for replica in replica_list:
                primary.add_replica(replica)

    def put(self, operation):
        node_name = operation[1]
        operation.pop(1)
        return self.nodes[node_name].put(operation)

    def get(self, operation):
        _, node_name, key = operation
        if node_name in self.nodes:
            return self.nodes[node_name].get(operation)

        if node_name == "any_node":  # go through each one
            for node_name in self.nodes:
                result = self.nodes[node_name].get(operation)
                if result != "null":
                    return result
        return "null"

    def sync(self, operation):
        _, from_node, to_node = operation
        _, from_keys = self.nodes[from_node].stats()
        for key in from_keys:
            if not self.nodes[to_node].has(key):
                item = self.nodes[from_node].fetch(key)
                self.nodes[to_node].put(item)

    def get_replication_status(self, operation):
        _, key = operation
        result = []
        for node_name in self.nodes:
            if self.nodes[node_name].has(key):
                result.append(node_name)
        return result

    def failover(self, operation):
        _, failed_node_name = operation
        for node_name in self.nodes:
            if node_name != failed_node_name:
                self.sync(["SYNC", failed_node_name, node_name])
    
    def apply(self, operation):
        action = operation[0]
        if action == "PUT":
            return self.put(operation)
        elif action == "GET":
            return self.get(operation)
        elif action == "SYNC":
            return self.sync(operation)
        elif action == "GET_REPLICATION_STATUS":
            return self.get_replication_status(operation)
        elif action == "FAILOVER":
            return self.failover(operation)

def assertEqual(a, b):
    if a != b:
        print(f"{a} != {b}")

def test():
    cache = Cache(2)
    # level 1, 2
    assertEqual(cache.apply(["GET", "a"]), "null")
    assertEqual(cache.apply(["PUT", "a", 1]), "stored")
    assertEqual(cache.apply(["GET", "a"]), 1)
    assertEqual(cache.apply(["PUT", "b", 2]), "stored")
    assertEqual(cache.apply(["GET", "b"]), 2)
    assertEqual(cache.apply(["PUT", "c", 3]), "evicted:a")
    assertEqual(cache.apply(["GET", "c"]), 3)
    assertEqual(cache.apply(["GET", "a"]), "null")
    print(cache.apply(["STATS"]))

    # level 3
    cache.apply(["PUT", "d", 4, 1, 10])
    cache.apply(["PUT", "e", 5, 1, 10])
    cache.apply(["PUT", "z", 5, 1, 1])
    print(cache.apply(["STATS"]))

    # level 4


test()