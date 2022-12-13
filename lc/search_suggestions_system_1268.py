from typing import List

class Node:
    def __init__(self, value):
        self.value = value
        self.matching = []
        self.succeeding = {}

    def display(self):
        return "(value={self.value}, matching={self.matching}, succeeding=\n\t{self.succeeding})".format(self=self)

    def __repr__(self):
        return self.display()

    def __str__(self):
        return self.display()

class Solution:
    """
    add node is a value, stores a list of matching strings, also a succeeding dict
    """
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        try:
            self.root = Node("")

            for product in products:
                current_node = self.root
                # add to current_node
                current_node.matching.append(product)

                for c in product:
                    if c not in current_node.succeeding:
                        new_node = Node(c)
                        current_node.succeeding[c] = new_node
                    current_node = current_node.succeeding[c]
                    current_node.matching.append(product)
            # print(self.root)

            result = []
            current_node = self.root
            for c in searchWord:
                if not current_node:
                    result.append([])
                    continue

                current_node = current_node.succeeding.get(c)
                if current_node:
                    result.append(sorted(current_node.matching)[:3])
                else:
                    result.append([])
            return result
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()
            import pdb; pdb.set_trace()

s = Solution()
products = ["mobile","mouse","moneypot","monitor","mousepad"]
searchWord = "mouse"
products = ["havana"]
searchWord = "havana"
s.suggestedProducts(products, searchWord)
        
