import copy
class DictDB(dict):
    """DictDB is a wrapper around dict"""
    def set(self, key, value):
        self[key] = value

    def _list_keys(self):
        return self.keys()

    def display(self):
        return str(self)

class DB:
    def __init__(self, db=None):
        self.db = db
        if not self.db:
            self.db = DictDB()
        self.transaction_stack = []

    def display(self):
        return "(db={self.db}, stack={self.transaction_stack})".format(self=self)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()

    def set(self, key, value):
        self.get_top_transaction().set(key, value)

    def get(self, key):
        # in reverse order, fetch key
        for data in self.transaction_stack[::-1]:
            if key in data:
                return data.get(key)
        return self.db.get(key)

    def _list_keys(self):
        return self.db._list_keys()

    def get_top_transaction(self):
        if self.transaction_stack:
            return self.transaction_stack[-1]
        else:
            return self.db

    def begin(self):
        self.transaction_stack.append(DictDB())

    def commit(self):
        data = copy.copy(self.get_top_transaction())
        self.transaction_stack.pop()
        current_top = self.get_top_transaction()
        for key in data._list_keys():
            current_top.set(key, data.get(key))
        print(self)

    def rollback(self):
        if self.transaction_stack:
            self.transaction_stack.pop()
        print(self)

db = DB()
db.set("a", 1)
db.begin()
db.set("a", 2)
db.begin()
db.set("b", 10)
db.commit()
db.rollback()
db.begin()
db.set("b", 15)
db.commit()
