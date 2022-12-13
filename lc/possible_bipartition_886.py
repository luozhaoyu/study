from typing import List

class Solution:
    def put(self, i, group_index):
        if i in self.group[group_index]:
            return True

        self.group[group_index].add(i)
        self.unallocated.discard(i)

        for j in self.dislike[i]:
            if j in self.group[group_index]:
                return False

            if not self.put(j, 1 - group_index):
                return False
        return True

    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        self.group = {0: set(), 1: set()}

        self.dislike = {}
        for i in range(n):
            self.dislike[i] = set()

        for dislike in dislikes:
            a, b = dislike[0]-1, dislike[1]-1
            self.dislike[a].add(b)
            self.dislike[b].add(a)

        self.unallocated = set(range(n))
        while self.unallocated:
            current = self.unallocated.pop()
            if not self.put(current, 0):  # put current people to group 0
                return False
        return True


s = Solution()
for n, dislikes in (
        (4,  [[1,2],[1,3],[2,4]]),
        (3,  [[1,2],[1,3],[2,3]]),
        (5, [[1,2],[2,3],[3,4],[4,5],[1,5]]),
):
    print(s.possibleBipartition(n, dislikes))
