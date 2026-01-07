import copy

class Record:
    """
    Record support:
    1. GET/SET with timestamp
    2. Backup and Restore operation

    Attributes:
        current: a {}, which holds current data: {"value": 1, "timestamp": 123}
        version: [], a list for storage: [(t1, v1), (t2, v2), (t3, v3)]
    """
    def __init__(self, value, timestamp):
        self.current = {
            "value": value,
            "timestamp": timestamp,
        }
        self.version = []

    def get(self, timestamp=None):
        if not self.current:  # no current value
            return None

        if self.current["timestamp"] and timestamp:
            if timestamp > self.current["timestamp"]:  # current > expiration -> None
                print("retrieving expired data, return None")
                return None

        # other logic: not both timestamp exists
        return self.current["value"]

    def set(self, value, timestamp=None):
        # if both timestamp exists, then compare
        if self.current and self.current["timestamp"] and timestamp:
            if self.current["timestamp"] < timestamp:
                self.current = {
                    "value": value,
                    "timestamp": timestamp
                }
            else:  # nothing happen, since the new timestamp is smaller
                print("skipping this set due to provided timestamp is too old")
                return ""

        # other logic: not both timestamp exists
        self.current = {
            "value": value,
            "timestamp": timestamp
        }
        return ""

    def backup(self, timestamp):
        """
        save a new snapshot for given timestamp
        """
        snapshot = copy.deepcopy(self.current)
        snapshot["timestamp"] = timestamp
        self.version.append(snapshot)

    def restore(self, timestamp):
        """
        go through the saved snapshots, find the latest snapshot that is <= timestamp
        """
        for i in range(len(self.version)):
            if self.version[-i]["timestamp"] <= timestamp:
                self.current = self.version[-i]
                return True
        return False

class Database:
    def __init__(self):
        """
        storage = {
            "fieldName": Record
        }
        Record = {
            "value": actual_value
            "timestamp"
        }
        """
        self.storage: [str, Record] = {}

    def set(self, field, value, timestamp=None):
        """
        if existing timestamp, no new timestamp -> proceed
        if no existing timestamp, new timestamp -> proceed
        if existing timestamp, new timestamp -> need to check
        """
        if not field in self.storage:
            self.storage[field] = Record(value, timestamp)
            return ""

        return self.storage[field].set(value, timestamp)

    def get(self, field, timestamp=None):
        if not field in self.storage:
            return None

        return self.storage[field].get(timestamp)

    def backup(self, timestamp):
        """backup each field accordingly
        """
        for value in self.storage.values():
            value.backup(timestamp)

    def restore(self, timestamp):
        for value in self.storage.values():
            value.restore(timestamp)

    def scan_range(self, min_value, max_value):
        sorted_keys = sorted(self.storage.keys())
        print(sorted_keys)
        find_insert_position_min = self.find_insert_position(sorted_keys, min_value)
        find_insert_position_max = self.find_insert_position(sorted_keys, max_value)
        print(find_insert_position_min, find_insert_position_max)
        return find_insert_position_max - find_insert_position_min

    def find_insert_position(self, arr, target):
        """binary search for insertion position in arr for target
        """
        left = 0
        right = len(arr)
        while left < right:
            mid = (left + right) // 2
            if arr[mid] == target:  # find exact match
                return mid
            elif target < arr[mid]:  # go to left part
                right = mid
            else:
                left = mid + 1
        return left


def test():
    db = Database()
    # level 1
    assert "" == db.set("f1", "v1")
    assert "v1" == db.get("f1")
    assert None == db.get("ffff")

    # level 2
    assert "" == db.set("a", 1, 1)
    assert "" == db.set("a", 3, 3)
    assert 3 == db.get("a", 2)
    assert None == db.get("a", 4)

    # level 3
    db.backup(3)
    assert "" == db.set("a", 5, 5)
    assert 5 == db.get("a", 5)
    assert 5 == db.get("a", 2)
    db.restore(3)
    assert 3 == db.get("a", 2)

    # level 4
    assert "" == db.set("c", 5)
    assert "" == db.set("b", 5)
    db.scan_range("a", "c")

    print("passed all tests")


test()