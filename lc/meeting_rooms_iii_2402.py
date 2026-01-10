from typing import List

class Solution:
    """
    1. always find the available meeting room
    1. always find the earliest meeting

    meeting_room_stats = [1, 3, 5]
    meeting_room_in_use = [[room_number, 0, 10], [1, 5], [2,7]]
        = [stats1, stats2, stats3]
    stats = [room_number, start_time, finish_time, held_meeting]
    meetings = []
    """
    def find_next_room(self, start_time):
        """
        find unused room with lowest number

        if finish_time <= start_time:
            return 0
        else:
            return finish_time
        """
        self.meeting_room_in_use.sort(key=lambda x: (x[2] if x[2] > start_time else 0, x[0]))
        return 0

    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        # make sure early meeting starts earlier
        meetings.sort()

        # initiate meeting room
        self.meeting_room_in_use = []
        for i in range(n):
            self.meeting_room_in_use.append([i, 0, 0, 0])

        result = [0 for i in range(n)]
        for meeting in meetings:
            print(self.meeting_room_in_use)
            # find next available room
            index = self.find_next_room(meeting[0])
            next_room = self.meeting_room_in_use[index]

            # count the result
            room_number = next_room[0]
            next_room[3] += 1
            result[room_number] += 1

            # schedule meeting in this room, adjust start time, and end time
            # new start time = max(previous_complete_time, meeting start time)
            next_room[1] = max(next_room[2], meeting[0])
            next_room[2] = next_room[1] + (meeting[1] - meeting[0])

        print(result)
        # output result
        max_meeting = 0
        max_room_number = 0
        i = 0
        while i < n:
            if result[i] > max_meeting:
                max_meeting = result[i]
                max_room_number = i
            i += 1
        return max_room_number


def test():
    n = 4
    meetings = [[18,19],[3,12],[17,19],[2,13],[7,10]]
    s = Solution()
    s.mostBooked(n, meetings)


test()
         