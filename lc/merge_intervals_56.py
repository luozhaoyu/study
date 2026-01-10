from typing import List

class Solution:
    """
    assume intervals are not overlapping, adding a new internal, how to keep it not overlapping
    1. for the sorted list, find the best position to insert the internal
    2. from that position, keep trying to merge low and high index
    """
    def merge_two_interval(self, intervals, left, right):
        if left < 0 or right >= len(intervals):  # return directly when out of range
            return right

        if intervals[right][0] <= intervals[left][1]:  # can merge
            intervals[left][1] = max(intervals[left][1], intervals[right][1])
            # pop the right
            intervals.pop(right)
            return left
        return right
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        result = []
        for interval in intervals:
            index = self.find_insertion_index(result, interval)
            # just insert first
            result.insert(index, interval)

            # try to merge left, only need to try once
            current_index = self.merge_two_interval(result, index-1, index)
            # print(current_index, result)

            # try to merge right
            while current_index + 1 < len(result) and result[current_index][1] >= result[current_index+1][0]:
                result[current_index][1] = max(result[current_index][1], result[current_index+1][1])
                # already merged, next one should be popped
                result.pop(current_index + 1)
            # print("done", result)


        return result

    def find_insertion_index(self, result: List[List[int]], interval: List[int]):
        """
        use binary search to find
        """
        low = 0
        high = len(result)
        while low < high:
            mid = (low + high) // 2
            # compare the first element
            if interval[0] < result[mid][0]:  # < middle element
                high = mid
            else:
                low = mid + 1  # ensure it can progress
        # print(f"inserting at {low} {result}")
        return low

def test():
    intervals = [[1,3],[2,6],[8,10],[15,18]]   
    intervals = [[1,4],[4,5]]
    intervals = [[4,7],[1,4]]
    intervals = [[1,3],[2,6],[8,10],[15,18], [3, 17]]   
    s = Solution()
    print(s.merge(intervals))

test()