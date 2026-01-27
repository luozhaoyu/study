from typing import *

class InMemoryDB:
    """
    Attributes:
        storage: {
            key: value
        }
        new_changes: {
            key: new_value | None
        }
    """
    def __init__(self):
        self.storage = {}
        self.new_changes = {}
        self.in_transaction = False
        
    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair."""
        if self.in_transaction:
            self.new_changes[key] = value
            return
        
        self.storage[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key. Returns None if not found."""
        if self.in_transaction:
            if key in self.new_changes:
                return self.new_changes[key]
        
        if self.exists(key):
            return self.storage[key]
        return None
    
    def delete(self, key: str) -> bool:
        """Delete a key. Returns True if existed, False otherwise."""
        if self.in_transaction:
            if key in self.new_changes or key in self.storage:
                result = True
            else:
                result = False
            self.new_changes[key] = None
            return result
        
        if self.exists(key):
            del self.storage[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        if self.in_transaction and key in self.new_changes:
            if self.new_changes[key] == None:  # new_changes would delete this key
                return False
            else:
                return True
        
        return key in self.storage
        
    def _in_transaction(self) -> bool:
        """whether it is in transaction"""
        pass
    
    def begin_transaction(self) -> None:
        """Start a new transaction.
        
        transaction: buffer all changes among transaction, then apply all changes
        together or abort all
        """
        self.new_changes = {}
        self.in_transaction = True
    
    def commit(self) -> None:
        """Commit current transaction.
        
        Apply all new_changes into storage
        """
        # go through each new_changes
        for key, value in self.new_changes.items():
            if value == None:  # means delete
                if key in self.storage:
                    del self.storage[key]
            else:
                self.storage[key] = value
        
        self.new_changes = {}
        self.in_transaction = False
    
    def rollback(self) -> None:
        """Rollback current transaction."""
        self.new_changes = {}
        self.in_transaction = False

"""
nested transaction:
* begin transaction -> create a new db -> multiple begin: need stack [{}, {}, {}], create another {}
* commit transaction -> apply new db back to this DB, mapA update mapB
* rollback transaction -> discard this new DB, stack.pop()
"""
class NestedDB(InMemoryDB):
    """
    Attributes:
        stack: [{}, {}]
    """
    def __init__(self):
        super().__init__()
        self.stack = [{}]
        
    def exists(self, key):
        for transaction in self.stack[::-1]:
            if key in transaction:
                return transaction[key] is not None
        return False
        
    def get(self, key):
        for transaction in self.stack[::-1]:
            if key in transaction:
                return transaction.get(key)
        return None
        
    def set(self, key, value):
        top_transaction = self.stack[-1]
        top_transaction[key] = value
        
    def delete(self, key):
        top_transaction = self.stack[-1]
        top_transaction[key] = None 
            
    def keys(self) -> List[Any]:
        result = []
        if self.in_transaction:
            result.extend(self.new_changes.keys())
            
        result.extend(self.storage.keys())
        return result
        
    def begin_transaction(self):
        self.stack.append({})
        
    def commit(self):
        if len(self.stack) < 2:
            print("error couldn't commit")
            return None
        top_transaction = self.stack[-1]
        inner_transaction = self.stack[-2]
        
        for key, value in top_transaction.items():
            if value == None:  # delete
                if key in inner_transaction:
                    del inner_transaction[key]
            else:
                inner_transaction[key] = value
        self.stack.pop()
        
    def rollback(self):
        self.stack.pop()

import time

class DBWithTTL(NestedDB):
    """
    Attributes:
        ttl = {
            key: expire_time
        }
    """
    def __init__(self):
        super().__init__()
        self.ttl = {}
        
    def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Set key with time-to-live in seconds."""
        self.ttl[key] = time.time() + ttl_seconds
        return super().set(key, value)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value. Returns None if expired or not found."""
        if key in self.ttl:
            if time.time() > self.ttl[key]:  # passed expire time
                if super().exists(key):
                    super().delete(key)
                return None
        return super().get(key)


def assert_equal(a, b):
    if a != b:
        print(f"error: {a} != {b}")

def test():
    # Example 1: Basic operations
    db = InMemoryDB()
    db.set("name", "Claude")
    assert_equal(db.get("name"), "Claude")     # Returns "Claude"
    assert_equal(db.exists("name"), True)       # Returns True
    assert_equal(db.delete("name"), True)       # Returns True
    assert_equal(db.get("name"), None)       # Returns None
    print(db.storage)
    print("passed 1")

    # Example 2: Transactions
    db.set("balance", 100)
    db.begin_transaction()
    db.set("balance", 50)
    assert_equal(db.get("balance"), 50)       # Returns 50 (in transaction)
    db.rollback()
    assert_equal(db.get("balance"), 100)    # Returns 100 (rollback successful)
    print(db.storage)
    print("passed 2")
    
    db = NestedDB()
    db.set("x", 1)
    db.begin_transaction()
    assert_equal(db.get("x"), 1)
    db.set("x", 2)
    db.begin_transaction()
    assert_equal(db.get("x"), 2)
    db.set("x", 3)
    assert_equal(db.get("x"), 3)
    db.rollback()  # x should be 2 in transaction
    assert_equal(db.get("x"), 2)
    db.get("x")     # Returns 2
    db.commit()     # x is now 2 in main DB
    print(db.stack)
    print("passed 3")
    
    db = DBWithTTL()
    db.set_with_ttl("session", "abc123", ttl_seconds=2)
    assert_equal(db.get("session"), "abc123")       # Returns "abc123"
    time.sleep(3)
    assert_equal(db.get("session"), None) # expired
    print("passed 4")
        
test()