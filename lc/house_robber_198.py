from typing import List

class Solution:
    """
    Algorithm:
      greedy as much as possible. Strategy can be reused. The strategy for house[i] is by:
    1. rob strategy: best strategy for f[i-2]
    2. no rob strategy: best strategy for f[i-1], f[i-2]
    3. f[i] >= f[i-1]
      f[i] = max(f_rob[i], f_skip[i])
      f_skip[i] = f[i-1]
      f_rob[i] = f_skip[i-1] + house[i]
    """
    def rob(self, nums: List[int]) -> int:
        f = []
        f_skip = []
        f_rob = []
        for i in range(len(nums)):
            house = nums[i]
            if i == 0:
                f_skip.append(0)
                f_rob.append(house)
            else:
                f_skip.append(f[i-1])
                f_rob.append(f_skip[i-1] + house)
            f.append(max(f_skip[i], f_rob[i]))
        print(f, f_skip, f_rob)
        return f[-1]

s = Solution()
nums = [1,2,3,1]
nums = [2,7,9,3,1]
s.rob(nums)
