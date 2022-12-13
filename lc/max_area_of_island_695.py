from typing import List

class Solution:
    """
    Algorithms:
    1. identify non-visited cells
    2. keep exploring connected cells, create a new island
    3. unless all cells are visited
    """
    def __init__(self):
        self.non_visited_cells = set()

    def get_non_visited_cells(self, grid):
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == 1:
                    self.non_visited_cells.add((x, y))

    def find_surrounding_cell(self, cell) -> List:
        top = (cell[0] - 1, cell[1])
        bottom = (cell[0] + 1, cell[1])
        left = (cell[0], cell[1] - 1)
        right = (cell[0], cell[1] + 1)

        result = []
        if top in self.non_visited_cells:
            result.append(top)
        if bottom in self.non_visited_cells:
            result.append(bottom)
        if left in self.non_visited_cells:
            result.append(left)
        if right in self.non_visited_cells:
            result.append(right)
        return result

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # initalize non-visited cells
        self.get_non_visited_cells(grid)

        result = 0

        while self.non_visited_cells:
            seed_cell = self.non_visited_cells.pop()
            # store current connected cells
            connected_cells = [seed_cell]
            # island represent connected cells
            current_island = set()
            current_island.add(seed_cell)

            # if has connected_cells, then keep searching
            while connected_cells:
                cell = connected_cells.pop()
                # mark it as visited
                self.non_visited_cells.discard(cell)
                current_island.add(cell)

                # add surrounding valid cell into connected_cells to be explored later
                connected_cells.extend(self.find_surrounding_cell(cell))

            # until no more connected_cells, record this island
            if len(current_island) > result:
                result = len(current_island)
        return result

s = Solution()
grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]

s.maxAreaOfIsland(grid)
        
