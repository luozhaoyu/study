"""
# Definition for an Interval.
class Interval:
    def __init__(self, start: int = None, end: int = None):
        self.start = start
        self.end = end
"""

class Solution:
    """
    Algorithm:
    1. sort interval by start, so can be certain no other interval in between
    2. merge the first to second interval
    """
    def merge_interval(self, early, late):
        # early and late disconnected
        if early.end < late.start:
            return late, Interval(early.end, late.start)

        # early and late overlaps
        early.end = max(early.end, late.end)
        return early, None

    def employeeFreeTime(self, schedule: '[[Interval]]') -> '[Interval]':
        flat = []
        for individual in schedule:
            for interval in individual:
                flat.append(interval)
        flat = sorted(flat, key=lambda x: x.start)
        i = 0
        current = flat[0]
        result = []
        while i + 1 < len(flat):
            i += 1
            current, free_time = self.merge_interval(current, flat[i])
            if free_time:
                result.append(free_time)
        return result
