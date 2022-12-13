from typing import List

class Solution:
    """
    Algorithms:
    1. iterate though intervals, try to insert into meeting room
    2. if no meeting room satisfied, add a new meeting room
    """
    def insert(self, interval, meeting_room):
        for existing_interval in meeting_room:
            if (interval[0] > existing_interval[0] and interval[0] < existing_interval[1]) or \
               (interval[1] > existing_interval[0] and interval[1] < existing_interval[1]) or \
               (existing_interval[0] > interval[0] and existing_interval[0] < interval[1]) or \
               (existing_interval[1] > interval[0] and existing_interval[1] < interval[1]) or \
               interval == existing_interval:
                return False
        meeting_room.append(interval)
        meeting_room = sorted(meeting_room, key=lambda x: x[0])
        return True
               
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:

        meeting_rooms = []
        for interval in intervals:
            can_insert = False
            for meeting_room in meeting_rooms:
                if self.insert(interval, meeting_room):
                    can_insert = True
                    break
            if not can_insert:  # need more meeting room
                meeting_rooms.append([interval])
        print(meeting_rooms)
        return len(meeting_rooms)

s = Solution()
intervals = [[0,30],[5,10],[15,20], [16,20], [17,20], [18,19], [19,20]]
s.minMeetingRooms(intervals)
