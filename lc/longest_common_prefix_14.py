from typing import List
class Node:
    def __init__(self, value, count=1):
        self.value = value
        self.count = count
        self.leaf = {}

    def display(self):
        return "(value={self.value}, count={self.count})\n\tleaf={self.leaf})".format(self=self)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()

class TrieTree:
    def __init__(self):
        self.root = Node("", count=0)

    def add_str(self, s):
        current_node = self.root
        current_node.count += 1
        for c in s:
            if c not in current_node.leaf:
                new_node = Node(c, count=0)
                current_node.leaf[c] = new_node
            current_node = current_node.leaf[c]
            current_node.count += 1
            

class Solution:
    """
    Algorithms:
    each str would construct a Trie path
    """
    def longestCommonPrefix(self, strs: List[str]) -> str:
        tree = TrieTree()
        for s in strs:
           tree.add_str(s) 
           print(tree.root)

        result = ""
        current_node = tree.root
        while True:
            found_common = False
            for c in current_node.leaf:
                node = current_node.leaf[c]
                if node.count == len(strs):
                    result += node.value
                    current_node = node
                    found_common = True
                    break
            if not found_common:
                return result

s = Solution()
test = ["flower","flow","flight", "fx"]
#test = ["dog","racecar","car"]
s.longestCommonPrefix(test)
        
