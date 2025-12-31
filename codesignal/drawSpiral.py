"""
Search algorithm to draw spiral
"""
from pprint import pprint


directions = [
    (0, 1),  # go right
    (1, 0),  # go down
    (0, -1),  # go left
    (-1, 0),  # go up
]

map = []


def solution(n, m, startCorner, indent, turns):
    """
    Args:
        n: number of lines
        m: number of rows

    draw clock wise spiral
    position: coordinate + direction
    while True:
        new_position, new_direction = find_next_position(position, direction)
        if position:
            draw
        else:
            return False
    """
    def within_boundary(x, y):
        if x < 0 or y < 0 or x >= n or y >= m:
            return False
        return True

    def is_occupied(x, y):
        if not within_boundary(x, y):
            return False

        return map[x][y] == "1"

    def is_valid_position(position, direction):
        """
        1. within boundary
        2. check indent
        """
        x, y = position
        if not within_boundary(x, y):
            return False

        if is_occupied(x + directions[direction][0] * indent,
            y  + directions[direction][1] * indent):
            return False

        if is_occupied(x + directions[(direction + 1) % 4][0] * indent,
            y  + directions[(direction + 1) % 4][1] * indent):
            return False

        if is_occupied(x + directions[(direction + 3) % 4][0] * indent,
            y  + directions[(direction + 3) % 4][1] * indent):
            return False
        return True
        

    def find_next_position(position, direction):
        """
        1. keep current direction, new_position
        2. check new_position within boundary and satisfy indent
        if not, try next direction

        Returns:
            new_position, new_direction
        """
        init_direction = direction
        while True:
            new_position = (position[0] + directions[direction][0],
            position[1] + directions[direction][1])
            if is_valid_position(new_position, direction):
                return new_position, direction
            else:
                direction = (direction + 1) % 4
                if direction == (init_direction + 2) % 4:  # it goes back to origin position
                    return False, False

    for _ in range(n):
        line = []
        for _ in range(m):
            line.append("0")
        map.append(line)

    startCoordinates = {
        1: ((0, 0), directions[0]),  # top-left, go right
        2: ((0, m-1), directions[1]),  # top-right, go down
        3: ((n-1, m-1), directions[2]),  # bottom-right, go left
        4: ((n-1, 0), directions[3]),  # bottom-left, go up
    }

    position, _ = startCoordinates[startCorner]
    direction = startCorner - 1
    x, y = position
    map[x][y] = "1"

    turns = turns * 4

    while True:
        position, new_direction = find_next_position(position, direction)
        if not position:
            return map

        # print(position, new_direction)
        if new_direction != direction:  # new turn
            turns -= 1
            print(turns)
            if turns == 0:
                return map
        direction = new_direction

        x, y = position
        map[x][y] = "1"



def test():
    n = 25
    m = 15
    startCorner = 1
    indent = 3
    turns = 3

    result = solution(n, m , startCorner, indent, turns)
    pprint(map)

test()