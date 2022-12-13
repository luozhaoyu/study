from typing import List

class Node:
    def __init__(self, val, whole_dict=None):
        self.val = val
        # key is char, value is next Node
        self.index = {}
        self.latest_val = None
        self.whole_dict = whole_dict

    def insert(self, word):
        """insert new word into Node
        1. check if first char in index, create if missing
        2. go to lower layer Node, update order
        """
        print(word)
        if not word:
            return True

        first_char = word[0]
        self.whole_dict.get(first_char)

        if self.latest_val and self.whole_dict.get(first_char).before(self.whole_dict.get(self.latest_val)):
            return False

        if first_char in self.index:
            return self.index[first_char].insert(word[1:])
        else:
            new_node = Node(first_char, whole_dict=self.whole_dict)
            self.index[first_char] = new_node

            # set order
            if not self.latest_val:
                self.latest_val = first_char
            else:
                self.whole_dict.get(self.latest_val).append(self.whole_dict.get(first_char))
                self.latest_val = first_char
            return new_node.insert(word[1:])

class WholeDict(dict):
    def get(self, key):
        if key in self:
            return self[key]

        self[key] = Char(key)
        return self[key]

class Char:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def append(self, next_char):
        self.next = next_char
        next_char.prev = self

    def before(self, char):
        next = self.next
        while next:
            if next.val == char.val:  # it is after char
                # print("False:", self.val, char.val)
                return True
            next = next.next
        return False

    def display(self):
        prev = self.prev.val if self.prev else None
        next = self.next.val if self.next else None
        return "({prev} -> {self.val} -> {next})".format(self=self, prev=prev, next=next)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()

class Solution:
    """
    Algorithm:
    1. build Trie node to get orders
    2. use order to form total order
    """
    def alienOrder(self, words: List[str]) -> str:
        whole_dict = WholeDict()
        root = Node("", whole_dict)
        for word in words:
            if not root.insert(word):  # invalid insert
                # print(whole_dict)
                return ""

        print(whole_dict)
        result = ""
        while whole_dict:
            _, random_char = whole_dict.popitem()
            result += random_char.val
            print(result)
            prev = random_char.prev
            next = random_char.next
            while prev:
                if not prev.val in result:
                    result = prev.val + result
                if prev.val in whole_dict:
                    del whole_dict[prev.val]
                prev = prev.prev

            while next:
                if not next.val in result:
                    result += next.val
                if next.val in whole_dict:
                    del whole_dict[next.val]
                next = next.next
        return result

s = Solution()        
words = ["zy", "zx"]
words = ["wrt","wrf","er","ett","rftt"]
words = ["z", "x", "z"]
words = ["ab", "adc"]
words = ["ac","ab","b"]
s.alienOrder(words)
