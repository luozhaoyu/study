from typing import List
import copy
class Solution:
    """
    Algorithm:
    backtrack to ensure all ticket will be used
    BFS will find the shortest one
    """
    def find_next_positions(self, position, past_tickets):
        remain_positions = copy.copy(self.possible_destinations.get(position))
        if not remain_positions:
            return []

        # remove position visited by previous ticket
        for past_ticket in past_tickets:
            start, end = past_ticket
            if start == position and end in remain_positions:
                # print(remain_positions, end)
                remain_positions.remove(end)

        # print(past_tickets, position, remain_positions)
        return sorted(remain_positions)

    def backtrack(self, position, past_tickets):
        # exit if all ticket used
        if past_tickets and len(past_tickets) == len(self.tickets):
            return past_tickets

        # find next possible position
        for next_position in self.find_next_positions(position, past_tickets):
            ticket = [position, next_position]
            past_tickets.append(ticket)
            result = self.backtrack(next_position, past_tickets)
            if result:
                return result
            # come back to try next one
            past_tickets.pop()
        
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        self.tickets = tickets
        self.possible_destinations = {}
        for ticket in tickets:
            start, end = ticket[0], ticket[1]
            if start in self.possible_destinations:
                self.possible_destinations[start].append(end)
            else:
                self.possible_destinations[start] = [end]
        # print(self.possible_destinations)
        result = self.backtrack("JFK", [])
        if not result:
            return result
        # print(result)
        return [ticket[0] for ticket in result] + [result[-1][-1]]

        
s = Solution()
tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
tickets = [["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]
tickets = [["EZE","AXA"],["TIA","ANU"],["ANU","JFK"],["JFK","ANU"],["ANU","EZE"],["TIA","ANU"],["AXA","TIA"],["TIA","JFK"],["ANU","TIA"],["JFK","TIA"]]
tickets = [["EZE","TIA"],["EZE","HBA"],["AXA","TIA"],["JFK","AXA"],["ANU","JFK"],["ADL","ANU"],["TIA","AUA"],["ANU","AUA"],["ADL","EZE"],["ADL","EZE"],["EZE","ADL"],["AXA","EZE"],["AUA","AXA"],["JFK","AXA"],["AXA","AUA"],["AUA","ADL"],["ANU","EZE"],["TIA","ADL"],["EZE","ANU"],["AUA","ANU"]]
s.findItinerary(tickets)
