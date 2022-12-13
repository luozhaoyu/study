from typing import List

class Node:
    def __init__(self, value, position):
        self.value = value
        self.position = position
        self.count = 1

        self.prev = None
        self.next = None
        self.parent = None

    def display(self):
        return "(value: {self.value}, position: {self.position}, count: {self.count})".format(self=self)

    def __str__(self):
        return self.display()

    def __repr__(self):
        return self.display()


class Solution:
    """
    Algorithm:
    1. remove node: O(1) remove by reference
    2. find and insert node: O(nlogn) binary search to find to insert

    Data Structure:
    linked list and index map (for removal and search)

    Algorithm2: use heap
    1. find: O(1)
    2. insert: O(logn)
    3. remove: O(logn)

    Attributes:
      index: key is value, return node
      head: always point to the biggest value
    """
    def __init__(self):
        self.head = None
        self.index = {}
        self.capacity = 0
        self.heap = []
        self.max_capacity = 0
        self.position = None

    def sift_up(self, node):
        position = node.position
        if position > 0:
            parent = self.heap[int((position-1) / 2)]
            if node.value > parent.value:  # swap with parent
                parent.position, node.position = node.position, parent.position
                # print("before swap", node, parent)
                self.heap[parent.position], self.heap[node.position] = self.heap[node.position], self.heap[parent.position]
                # parent, node = node, parent
                # print("after swap", node, parent)
                self.sift_up(node)

    def sift_down(self, node):
        left = None
        right = None
        position = node.position
        if position * 2 + 1 < len(self.heap):
            left = self.heap[position * 2 + 1]
        if position * 2 + 2 < len(self.heap):
            right = self.heap[position * 2 + 2]

        if not left and not right:
            return

        larger_child = left
        # child_index = position * 2 + 1
        if right and self.is_smaller(left, right):
            larger_child = right
            # child_index = position * 2 + 2

        if self.is_smaller(node, larger_child):
            new_position = larger_child.position
            self.swap(node.position, larger_child.position)
            self.sift_down(self.heap[new_position])

    def is_smaller(self, node_a, node_b):
        if node_a.count == 0:
            return True
        if node_b.count == 0:
            return False
        return node_a.value < node_b.value

    def insert_node(self, value, previous_value):
        # remove firstly
        if self.capacity == self.max_capacity:
            if previous_value is not None:
                self.remove_node(previous_value)

        self.capacity += 1
        if value in self.index:
            self.index[value].count += 1
            return

        new_node = Node(value, len(self.heap))
        self.index[value] = new_node
        self.heap.append(new_node)
        self.sift_up(new_node)


    def swap(self, position_a, position_b):
        #print("swap", position_a, position_b, self.heap)
        self.heap[position_a].position, self.heap[position_b].position = self.heap[position_b].position, self.heap[position_a].position
        self.heap[position_a], self.heap[position_b] = self.heap[position_b], self.heap[position_a]
        # print("swapped", self.heap)

    def remove_node(self, value):
        """
        1. reduce counter
        2. sift_down the node
        3. swap with latest node
        4. sift_up the latest node
        5. pop if necessary
        """
        if value in self.index:
            self.index[value].count -= 1
            self.capacity -= 1
            if self.index[value].count == 0:  # need to remove this node
                self.sift_down(self.index[value])

                sift_down_position = self.index[value].position
                self.swap(len(self.heap) - 1, sift_down_position)

                self.sift_up(self.heap[sift_down_position])

                pop_node = self.heap.pop()
                del self.index[pop_node.value]

    def get_max_node(self):
        return self.heap[0].value

    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        self.max_capacity = k
        previous_value = None
        result = []
        for i in range(len(nums)):
            if i - k >= 0:
                previous_value = nums[i-k]
            self.insert_node(nums[i], previous_value)
            if self.capacity == self.max_capacity:
                result.append(self.get_max_node())
            print(i, nums[i], previous_value, self.heap, self.get_max_node())
        return result

s = Solution()
nums = [-5769,-7887,-5709,4600,-7919,9807,1303,-2644,1144,-6410,-7159,-2041,9059,-663,4612,-257,2870,-6646,8161,3380,6823,1871,-4030,-1758,4834,-5317,6218,-4105,6869,8595,8718,-4141,-3893,-4259,-3440,-5426,9766,-5396,-7824,-3941,4600,-1485,-1486,-4530,-1636,-2088,-5295,-5383,5786,-9489,3180,-4575,-7043,-2153,1123,1750,-1347,-4299,-4401,-7772,5872,6144,-4953,-9934,8507,951,-8828,-5942,-3499,-174,7629,5877,3338,8899,4223,-8068,3775,7954,8740,4567,6280,-7687,-4811,-8094,2209,-4476,-8328,2385,-2156,7028,-3864,7272,-1199,-1397,1581,-9635,9087,-6262,-3061,-6083,-2825,-8574,5534,4006,-2691,6699,7558,-453,3492,3416,2218,7537,8854,-3321,-5489,-945,1302,-7176,-9201,-9588,-140,1369,3322,-7320,-8426,-8446,-2475,8243,-3324,8993,8315,2863,-7580,-7949,4400],6
s.maxSlidingWindow([7629, 5877, 3338, 8899, 4223, -8068, 3775, 7954, 8740, 4567, 6280, -7687, -4811, -8094, 2209], 6)
        
