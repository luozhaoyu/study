from typing import Optional, List
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.single_path_cache = {}
        self.double_path_cache = {}
    def create_tree_for_max_sum(self, tree_list: List):
        """
        build tree firstly:
        use queue to store nodes needs to append child: [parent, left, right]
        pop out parent every new left and right
        """
        root = TreeNode(tree_list[0])
        self.root = root
        queue = [root]
        counter = 0
        for i in tree_list[1:]:
            counter += 1
            if i == "null":  # skip
                if counter == 2:
                    counter = 0
                    queue.pop(0)
                continue

            # i is a new node
            new_node = TreeNode(i)
            queue.append(new_node)

            # append it as left or right
            if counter == 1:
                queue[0].left = new_node
            if counter == 2:
                queue[0].right = new_node
                counter = 0
                queue.pop(0)
        return self.maxPathSum(root)
        

    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        if root in self.double_path_cache:
            return self.double_path_cache[root]

        left = self.max_single_path(root.left)
        right = self.max_single_path(root.right)
        result = max(root.val + left + right, root.val, root.val + left, root.val + right)
        if root.left:
            result = max(result, self.maxPathSum(root.left))
        if root.right:
            result = max(result, self.maxPathSum(root.right))

        self.double_path_cache[root] = result
        return result

    def max_single_path(self, root: Optional[TreeNode]) -> int:
        """return the max single path of a tree"""
        if not root:
            return 0

        if root in self.single_path_cache:
            return self.single_path_cache[root]

        result = max(0, root.val)
        if root.left:
            left = self.max_single_path(root.left)
            result = max(result, left + root.val)
        if root.right:
            right = self.max_single_path(root.right)
            result = max(result, right + root.val)

        self.single_path_cache[root] = result
        return result
            
        

s = Solution()
"""
  -1
 5
4
  2
-4
"""
s.create_tree_for_max_sum([-1,5,"null",4,"null","null",2,-4])

