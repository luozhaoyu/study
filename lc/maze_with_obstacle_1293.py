from typing import List

class Solution:
    """
    Algorithm:
    if we know the min_step(x, y), then we can calculate its surrounding cell
    1. get current grid, calculate the surrounding cell
    2. add surrounding cell to the queue
    """
    def is_shorter(self, current_grid, next_grid):
        """
        Returns:
          True: current_grid -> next_grid is shorter
        """
        is_shorter = False
        if next_grid not in self.min_step:
            self.min_step[next_grid] = {}
            is_shorter = True

        is_wall = 1 if self.grid[next_grid[0]][next_grid[1]] else 0

        # iterate all current_grid step
        for step, can_eliminate in self.min_step[current_grid].items():
            new_eliminate = can_eliminate - is_wall
            if step + 1 not in self.min_step[next_grid] and new_eliminate >= 0:  # has no such solution
                self.min_step[next_grid][step + 1] = can_eliminate - is_wall
                is_shorter = True
                continue

            if step + 1 in self.min_step[next_grid] and can_eliminate - is_wall > self.min_step[next_grid][step + 1]:  # find shorter path
                self.min_step[next_grid][step + 1] = can_eliminate - is_wall
                is_shorter = True
                continue

        return is_shorter

    def update_surrouding_grids(self, current_grid):
        if not self.min_step.get(current_grid):  # skip if current is empty
            return []

        updated_grids = set()
        for grid in self.find_surrouding_grids(current_grid):
            if self.is_shorter(current_grid, grid):
                updated_grids.add(grid)
        return list(updated_grids)

    def find_surrouding_grids(self, current_grid):
        # find all valid surrounding grids
        neighbour_offsets = (
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
        )
        grids = set()
        for offset in neighbour_offsets:
            x, y = current_grid[0] + offset[0], current_grid[1] + offset[1]
            # check coordinate is valid
            if x >= 0 and y >= 0 and x < len(self.grid) and y < len(self.grid[0]):
                grids.add((x, y))
        return list(grids)

    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        self.grid = grid

        for line in self.grid:
            print(line)

        # return self.shortestPath_with_recursion(grid, k)

        # key is (x, y), value is dict of solution { step1: num_obstacles_can_eliminate, step2: num_obstacles_can_eliminate }
        self.min_step = {
            (0, 0): {
                0: k
            }
        }

        queue = [(0, 0)]

        while queue:
            # pop current grid, BFS
            current_grid = queue.pop(0)

            # exit if grid is (m-1, n-1)
            if current_grid == (len(grid) - 1, len(grid[0]) - 1):
                print(current_grid, self.min_step.get(current_grid), self.min_step)
                if self.min_step.get(current_grid):
                    return sorted(self.min_step.get(current_grid, {-1: None}))[0]
                return -1

            # calculate its surrounding grids
            surrounding_grids = self.update_surrouding_grids(current_grid)

            # add surrounding grids into queue
            queue.extend(surrounding_grids)


        # did not return even though the queue is exhausted -> no answer
        return -1

    def shortest_path(self, current_grid):
        """
        Returns:
          solution: dict (key is step, value is wall_to_eliminate)
        """
        if current_grid in self.cache:
            return self.cache[current_grid]

        self.stack.add(current_grid)
        solution = {}
        
        is_wall = 1 if self.grid[current_grid[0]][current_grid[1]] else 0

        # find all neighbouring grids
        neighbouring_grids = self.find_surrouding_grids(current_grid)

        for next_grid in neighbouring_grids:
            if next_grid in self.stack:  # already in stack, no need to deep dive
                continue
            neighbouring_solution = self.shortest_path(next_grid)
            # iterate all the solution
            for step, wall_to_eliminate in neighbouring_solution.items():
                new_eliminate = wall_to_eliminate - is_wall
                if new_eliminate < 0:
                    continue
                if step + 1 not in solution:  # new route found
                    solution[step+1] = new_eliminate
                    continue

                if new_eliminate > solution[step+1]:  # better solution
                    solution[step+1] = new_eliminate

        print(current_grid, solution, neighbouring_grids, self.cache)
        self.cache[current_grid] = solution
        return solution


    def shortestPath_with_recursion(self, grid: List[List[int]], k: int) -> int:
        """
        f(x,y) = iterate all steps from neighbouring grids 
        """
        self.cache = {
            (0, 0): {
                0: k
            }
        }
        # store current grids on the stack
        self.stack = set()
        solution = self.shortest_path((len(grid) - 1, len(grid[0]) - 1))
        print(self.cache)
        return solution


s = Solution()
grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]
grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]
#grid = [[0,1,1],[1,1,1],[1,0,0]]
grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
grid = grid[:9]
k = 5
s.shortestPath(grid, k)
