from typing import List


class Node:
    def __init__(self, value, layer=0):
        self.value = value
        self.count = 1  # how many identical items
        self.left = None
        self.right = None
        self.member = 1  # how many members in the tree
        self.layer = layer  # current layer
        self.parent = None

    def display(self):
        return "({self.value}, {self.count}, {self.member}, left={left}, right={right})".format(self=self, left=self.left and self.left.value, right=self.right and self.right.value)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()


class BinarySearchTree:
    """
    a
    | \
    b  c 
    |  |
    d  e
    """
    def __init__(self, value):
        self.root = Node(value)
        self.display_layers = {0: [self.root]}
    
    def find_value(self, value):
        """find how many values smaller than this value"""
        smaller = 0
        current_node = self.root
        while True:
            if current_node.value == value:  # add all left node
                if current_node.left:  # has left node
                    smaller += current_node.left.member
                    return smaller
                else:  # no left node, return directly
                    return smaller
            elif current_node.value < value:  # left side is smaller, check right side
                smaller += current_node.count
                if current_node.left:  # has left node
                    smaller += current_node.left.member
                if current_node.right:
                    current_node = current_node.right
                else:  # no right node, return directly
                    return smaller
            else:  # smaller than current node, check its left
                if current_node.left:
                    current_node = current_node.left
                else:  # no left node, that's it
                    return smaller

    def attach_child_node(self, current_node, value):
        new_layer = current_node.layer + 1
        new_node = Node(value, layer=new_layer)
        new_node.parent = current_node

        # display
        if new_layer in self.display_layers:
            self.display_layers[new_layer].append(new_node)
        else:
            self.display_layers[new_layer] = [new_node]

        self.increase_member(new_node)
        return new_node

    def increase_member(self, node):
        while node.parent:
            node.parent.member += 1
            node = node.parent

    def add_node(self, value):
        """
        if value is smaller, go left
        if value is larger, go right

        increase the member for the corresponding node
        """
        current_node = self.root

        while True:
            if current_node.value == value:
                current_node.count += 1
                current_node.member += 1
                self.increase_member(current_node)
                return

            if value < current_node.value:  # go left
                if current_node.left is None:  # add as left node
                    new_node = self.attach_child_node(current_node, value)
                    current_node.left = new_node
                    return
                else:
                    current_node = current_node.left
            else:  # go right
                if current_node.right is None:  # add as left node
                    new_node = self.attach_child_node(current_node, value)
                    current_node.right = new_node
                    return
                else:
                    current_node = current_node.right

    def display(self):
        print(self.display_layers)
        for layer in sorted(self.display_layers):
            print("layer={}".format(layer), "\t".join([str(item) for item in self.display_layers[layer]]))
        


class Solution:
    """
    solution A: O(n*n)
    f(list[0..n]) = f(list[0..n-1]) + find_reverse_paris(list[n], list[0..n-1]) 

    solution B: O(nlogn) ?
    for each value, how to quickly find number of items less than that?
    wrong: the order is different with BST
    binary search tree: if we have a tree, log(n) find how many items > 2 num[j] 
    -> O(n) * O(logn(n)
    space complexity is O(n)

    can BST find how many smaller or larger items?
    root node contain all count
    go to right, means larger than left count
    go to left, means undecided

    solution C:
    [2, 4, 3, 5, 1] -> [2, 4, 3] [5, 1]
    if we know f([2, 4, 3]) = f([2, 3, 4]), which would not affect final result
    f(2) -> in [2, 4, 3] how many items < 2 / 2 = 1
    f'(2) = f(2) + {[5, 1] how many items < 2 / 2 = 1}
        for each item x, if x < 2 / 2 = 1, then f'(2) += 1

    1. break into smaller list, calculate each list reversePairs: f(l)
    2. sort each smaller list
    3. when merge two smaller list l1 and l2 into l3:
        f(l3) = f(l1) + f(l2) + reversePairs(x, y) that x in l1, y in l2
        optimization: find the smaller among (x,y), loop through x
        for x in l1:
            f(l3) += how many values in l2 < x / 2
    """
    def reversePairs(self, nums: List[int]) -> int:
        if len(nums) == 0:
            return 0
        return self.reversePairs(nums[:-1]) + self.find_reverse_paris(nums[:-1], nums[-1])

    def find_reverse_paris(self, nums: List[int], value: int):
        count = 0
        for i in nums:
            if i > 2 * value:
                count += 1
        return count


class SolutionC:
    def reversePairs(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return 0

        if len(nums) == 2:
            if nums[0] > 2 * nums[1]:
                return 1
            else:
                return 0

        # break into 2 pieces
        middle = int(len(nums) / 2)
        l1 = nums[:middle]
        l2 = nums[middle:]
        return self.reversePairs(l1) + self.reversePairs(l2) + self.find_inter_list_reverse_pairs(l1, l2)

    def find_inter_list_reverse_pairs(self, l1: list[int], l2: list[int]) -> int:
        l1.sort()
        result = 0
        # TODO: loop through l2 is faster
        for i in l1:
            # find how many values fit i > 2 * j -> j < i / 2
            result += self.find_number_of_items_less_than(i / 2.0, l2)
        return result

    def find_number_of_items_less_than(self, value, l2):
        """find j < value

        Algo: use binary search for sorted list
        find left < value <= left + 1
        """
        l2.sort()
        # find items < value
        left = 0
        right = len(l2) - 1
        if value <= l2[left]:  # every item is larger
            return 0
        if value > l2[right]:  # every item is smaller
            return len(l2)
            
        # value is in the middle
        while left < right:
            middle = int((left + right) / 2)
            if right == left + 1:
                return left + 1
            if l2[middle] == value:
                right = middle
            elif l2[middle] > value:
                right = middle
            else:
                left = middle



def test():
    s = Solution()
    nums = [1,3,2,3,1]
    print(s.reversePairs(nums))
    """
    2
    1  4
    3 5
    """
    nums = [2,4,3,5,1]
    print(s.reversePairs(nums))
    nums = [2566,5469,1898,127,2441,4612,2554,5269,2785,5093,3931,2532,1195,1101,1334,2124,1156,3400,747,5046,3325,4039,1858,3655,4904,2255,1822,972,5175,2880,2776,4900,2172,3808,3441,4153,3969,3116,1913,5129,4839,4586,752,1804,1970,4052,5016,3781,5000,4331,2762,4886,826,1888,1175,2729,1610,1634,2773,543,2617,4990]
    nums = [5000, 4000, 500, 3000, 2000, 1000, 300, 1000]
    # print(s.reversePairs(nums))
    bst = BinarySearchTree(nums[0])
    for i in nums[1:]:
        bst.add_node(i)

    bst.display()
    print("find {} index: {}".format(2000, bst.find_value(2000)))
    print("find {} index: {}".format(1000, bst.find_value(1000)))

s = SolutionC()
for test in (
        [1,3,2,3,1],
        [2,4,3,5,1],
        [2566,5469,1898,127,2441,4612,2554,5269,2785,5093,3931,2532,1195,1101,1334,2124,1156,3400,747,5046,3325,4039,1858,3655,4904,2255,1822,972,5175,2880,2776,4900,2172,3808,3441,4153,3969,3116,1913,5129,4839,4586,752,1804,1970,4052,5016,3781,5000,4331,2762,4886,826,1888,1175,2729,1610,1634,2773,543,2617,4990]
):
    print(s.reversePairs(test))
