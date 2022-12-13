from typing import List

class Solution:
    """
    Algorithm:
    1. split the array into subarrays that all items are less than right
    2. calculate the corresponding subarrays
    """
    def count_subarrays(self, array):
        if len(array) == 0:
            return 0

        first = array[0]
        if len(array) == 1:
            if first >= self.left:
                return 1
            return 0

        if first >= self.left:  # subarrays contains the first item or not
            result = self.count_subarrays(array[1:]) + len(array)
            print(array, result)
            return result

        count = 0
        for i in array[1:]:
            if i >= self.left and i <= self.right:
                count += 1
        result = count + self.count_subarrays(array[1:])
        print(array, result)
        return result


    def numSubarrayBoundedMax(self, nums: List[int], left: int, right: int) -> int:
        result = 0
        i = 0
        self.left = left
        self.right = right
        while i < len(nums):
            # count continuous nums within the range
            array = []
            while i < len(nums) and nums[i] <= right:
                array.append(nums[i])
                i += 1
            result += self.count_subarrays(array)
            print(result, array)
            i += 1
        return result


s = Solution()
nums = [2,1,4,3]
nums = [2,9,2,5,6, 9, 1, 2, 5, 6]
nums = [73,55,36,5,55,14,9,7,72,52]
left = 2
left = 32
right = 8
right = 69
s.numSubarrayBoundedMax(nums, left, right)
