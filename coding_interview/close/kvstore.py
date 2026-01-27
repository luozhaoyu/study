"""
6:00
"""
from typing import *
import pickle
import os
import copy

class PickleKVStore:
    def __init__(self):
        self.storage = {}

    def set(self, key: str, value: Any) -> None:
        """Store a key-value pair"""
        self.storage[key] = value

    def get(self, key: str) -> Any:
        """Retrieve a value by key"""
        return self.storage[key]

    def delete(self, key: str) -> bool:
        """Remove a key-value pair"""
        if key in self.storage:
            del self.storage[key]
            return True
        return False

    def snapshot(self) -> bytes:
        """Serialize entire store state to bytes"""
        return pickle.dumps(self.storage)

    def restore(self, data: bytes) -> None:
        """Restore store from serialized snapshot"""
        self.storage = pickle.loads(data)


class KVStore(PickleKVStore):
    """
    - snapshot complete within O(n)
    - concurrent reads during snapshot

    snapshot:
    1. serilization -> CPU heavy -> multiprocessing > multi-threading
    2. persistence -> IO heavy

    concurrency: create a new background process
    when new read comes in, main process doesn't block
    new process can access the same data -> multiprocessing.Manager()
    """
    def snapshot(self) -> bytes:
        """
        multiprocessing: fork a child proces
        """
        pid = os.fork()
        if pid == 0:  # child process for snapshot
            print("I'm {}, a newborn that for snapshot!".format(os.getpid()))
            return self._snapshot(self.storage)
        else:  # old process
            print("I'm the dad of {}, and he knows to use the terminal!".format(pid))
            os.waitpid(pid, 0)

    def _snapshot(self, data) -> bytes:
        return pickle.dumps(data)

    def _restore(self, data: bytes) -> None:
        """Restore store from serialized snapshot"""
        return super().restore(data)

    def restore(self, data: bytes) -> None:
        pid = os.fork()
        if pid == 0:  # child process for restore
            print("I'm {}, a newborn that for restore!".format(os.getpid()))
            return self._restore(data)
        else:  # old process
            print("I'm the dad of {}!".format(pid))
            os.waitpid(pid, 0)

class KVStoreTransaction(KVStore):
    """
    start a transaction
    commit a transaction
    rollback a transaction
    """
    def __init__(self):
        super().__init__()
        self.transaction = None

    def begin_transaction(self):
        self.transaction = {}

    def commit(self):
        if not self.transaction:
            return
        for key, value in self.transaction.items():
            if value == None:
                self.delete(key)
            else:
                self.set(key, value)

    def rollback(self):
        self.transaction = None

    def in_transaction(self):
        return self.transaction is not None

    def set(self, key: str, value: Any) -> None:
        if self.in_transaction():
            self.transaction[key] = value
            return
        return super().set(key, value)

    def get(self, key: str) -> Any:
        if self.in_transaction():
            if key in self.transaction:
                return self.transaction[key]
        return super().get(key)

    def delete(self, key: str) -> bool:
        if self.in_transaction():
            if key in self.transaction:
                self.transaction[key] = None
        return super().delete(key)


class KVStoreIncrementalSnapshot(KVStore):
    """
    incremental snapshot: changed data = current data - previous_snapshot

    snapshot: version, changes
    Attribute:
        previous_snapshot: {}
    """
    def __init__(self):
        self.previous_snapshots: List[Dict] = []
        self.last_storage = None
        super().__init__()

    def get_incremental_data(self) -> Dict:
        """incremental = current - previous"""
        if not self.previous_snapshot:
            return self.storage

        change_data = {}
        for key, value in self.storage:
            if key in self.last_storage and self.last_storage[key] != value:
                change_data[key] = value
        return change_data

    def snapshot(self):
        change_data = self.get_incremental_data()
        try:
            result = self._snapshot(change_data)
            self.previous_snapshot.append(change_data)
            self.last_storage = copy.deepcopy(self.storage)
            return result
        except Exception as e:
            print("error during snapshot")
            raise e



def test_single_obj(obj):
    store = KVStore()
    store.set("test", obj)
    serialized_data = store.snapshot()

    new_store = KVStore()
    new_store.restore(serialized_data)
    result = new_store.get("test")
    if obj != result:
        raise Exception(f"test failed: {obj} != {result}")

def unit_test():
    test_list = [0, 1, -1, 1.5, -2.3, "abc"]
    for test in test_list:
        test_single_obj(test)

    test_single_obj(test_list)
    test_single_obj({"a": 123, "bc": "xyz"})
    print("unit test passed!")

unit_test()

def test1():
    store = KVStore()
    store.set("user:123", {"name": "Alice", "credits": 100})
    store.set("model:gpt4", {"tokens": 8192, "temperature": 0.7})
    snapshot_data = store.snapshot()
    print(f"debug: {snapshot_data}")
    store.delete("user:123")
    store.restore(snapshot_data)
    assert store.get("user:123") == {"name": "Alice", "credits": 100}
    print("passed test1")


def test2():
    store = KVStore()
    store.set("list_data", [1, 2, [3, 4]])
    store.set("set_data", {1, 2, 3})
    snapshot_data = store.snapshot()
    new_store = KVStore()
    new_store.restore(snapshot_data)
    assert new_store.get("list_data") == [1, 2, [3, 4]]
    assert new_store.get("set_data") == {1, 2, 3}
    print("passed test2")


test1()
test2()