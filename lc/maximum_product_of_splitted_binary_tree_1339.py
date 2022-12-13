from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        # None means this node has not calculated the sum_value
        self.sum_value = None

    def calculate_sum_value(self):
        if self.sum_value is not None:  # already calculated previously
            return self.sum_value

        # initialize
        self.sum_value = self.val

        if self.left and self.left != "null":
            self.sum_value += self.left.calculate_sum_value()
        if self.right and self.right != "null":
            self.sum_value += self.right.calculate_sum_value()

        return self.sum_value

    def traverse(self, solution):
        # determine if it is a better solution:
        if abs(solution.half_value - solution.closest_half_value) > abs(solution.half_value - self.sum_value):
            solution.closest_half_value = self.sum_value
        if self.left and self.left != "null":
            self.left.traverse(solution)
        if self.right and self.right != "null":
            self.right.traverse(solution)

    def debug(self):
        return "(val={self.val}, sum={self.sum_value}, left={left}, right={right})".format(self=self, left=self.left, right=self.right)

    def __str__(self):
        return self.debug()

    def __repr__(self):
        return self.debug()

class Tree:
    def __init__(self, root: TreeNode):
        self.values = {}

        self.calculate_sum_value(root)

        # init: get total value / half value
        self.half_value = self.values[root] / 2
        self.closest_half_value = self.half_value * 2


    def calculate_sum_value(self, node: TreeNode):
        if node in self.values:  # already calculated previously
            return self.values[node]

        # initialize
        value = node.val

        if node.left and node.left != "null":
            value += self.calculate_sum_value(node.left)
        if node.right and node.right != "null":
            value += self.calculate_sum_value(node.right)

        self.values[node] = value
        return self.values[node]

    def traverse(self, node):
        # determine if it is a better solution:
        if abs(self.half_value - self.closest_half_value) > abs(self.half_value - self.values[node]):
            self.closest_half_value = self.values[node]
        if node.left and node.left != "null":
            self.traverse(node.left)
        if node.right and node.right != "null":
            self.traverse(node.right)

class Solution:
    """
    Algorithm:
    to maximum the product: it needs to be as average as possible
    a + b >= 2 *sqrt(ab)

    If we could know the sum of all nodes under the Tree -> find the node that is mostly close to half sum of the whole tree
    0. construct the tree from list
      for root[i] its parent is root[(i-1)/2]
    1. calculate sums for all node
    2. O(n) iterate through all node

    """
    def __init__(self):
        self.closest_half_value = None
        self.half_value = None

    def construct_then_maxize_tree(self, values): 
        for i in range(len(values)):
            print(values)
            if values[i] == "null":
                continue
            new_node = TreeNode(values[i])
            values[i] = new_node

            if i % 2 == 0: ## the right child of parent node (i-1) / 2
                values[int((i - 1) / 2)].right = new_node
            else:
                values[int((i - 1) / 2)].left = new_node
        return self.maxProduct(values[0])

    def construct_tree_via_stack(self, values):
        """
        Algorithm:
        always fetch the first node to add child -> use stack
        """
        new_node = TreeNode(values[0])
        root = new_node
        stack = [new_node]

        for i in values[1:]:
            current_node = None
            # fetch the first node
            if stack:
                current_node = stack[0]

            # add as its child
            if current_node:
                if i == "null":
                    new_node = "null"
                else:  # add valid child to stack
                    new_node = TreeNode(i)
                    stack.append(new_node)
                if current_node.left is None:
                    current_node.left = new_node
                elif current_node.right is None:
                    current_node.right = new_node
                    # pop out the current_node, as it is full now
                    stack.pop(0)
            print(i, stack)
        return self.maxProduct(root)
                

    def maxProduct_via_treenode(self, root: Optional[TreeNode]) -> int:
        # get total value / half value
        self.half_value = root.calculate_sum_value() / 2
        self.closest_half_value = self.half_value * 2

        # traverse tree to find answer
        root.traverse(self)

        return int((self.half_value * 2 - self.closest_half_value) * self.closest_half_value)

    def maxProduct(self, root: Optional[TreeNode]) -> int:
        tree = Tree(root)

        # traverse tree to find answer
        tree.traverse(root)

        return int((tree.half_value * 2 - tree.closest_half_value) * tree.closest_half_value) % (10 ** 9 + 7)

s = Solution()
root = [1,"null",2,3,4,"null","null",5,6]
root = [1,2,3,4,5,6]
print(s.construct_tree_via_stack(root))
