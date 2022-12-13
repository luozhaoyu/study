import random

class Heap(list):
    def insert(self, value):
        self.append(value)
        self.sift_up(len(self) - 1)

    def sift_up(self, index):
        """swap node with parent if criteria meets, ensure the top one meets the criteria mostly"""
        parent_index = int((index - 1) / 2)
        
        if self[index] < self[parent_index]:
            self[index], self[parent_index] = self[parent_index], self[index]
            self.sift_up(parent_index)

    def sift_down(self, index):
        """swap with the most satisfying left or right child"""
        left_index = index * 2 + 1
        right_index = index * 2 + 2

        # if left is better
        if left_index < len(self) and self[left_index] < self[index]:
            if (right_index < len(self) and self[left_index] <= self[right_index]) or (right_index >= len(self)):
                self[index], self[left_index] = self[left_index], self[index]
                # keep digging down
                self.sift_down(left_index)

        # if right is betterr
        if right_index < len(self) and self[right_index] <= self[left_index] and self[right_index] < self[index]:
            self[index], self[right_index] = self[right_index], self[index]
            self.sift_down(right_index)

    def pop_top(self):
        result = self[0]
        self[0] = self[len(self) - 1]
        self.pop()
        self.sift_down(0)
        return result

    def sort_it(self):
        """always put the top node to the bottom, then sift_down"""
        res = []
        for i in range(len(self)):
            res.append(self.pop_top())
        return res


h = Heap()
for i in range(10):
    l = random.sample(range(10), 5) + random.sample(range(10), 5) 
    for i in l:
        h.insert(i)
    res = h.sort_it()
    assert res == sorted(res)
    print(l, res, sorted(res))

