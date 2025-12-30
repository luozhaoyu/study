import copy

def is_pair_solution(head, tail):
    if head == tail:
        return True

    if head:  # string1 is not empty, so it can move to string2
        if head[:-1] == head[-1] + tail:
            return True
    if tail:
        if head + tail[0] == tail[1:]:
            return True
    return False

def move_head_left(arr):
    item1 = arr[0]
    item2 = arr[1]
    rest = copy.deepcopy(arr[2:])
    result = [item1 + item2[0], item2[1:]]
    result.extend(rest)
    return result

def move_head_right(arr):
    item1 = arr[0]
    item2 = arr[1]
    rest = copy.deepcopy(arr[2:])
    result = [item1[:-1], item1[-1] + item2]
    result.extend(rest)
    return result

def move_tail_left(arr):
    item1 = arr[-2]
    item2 = arr[-1]
    rest = copy.deepcopy(arr[:-2])
    result = rest
    result.extend([item1 + item2[0], item2[1:]])
    return result

def move_tail_right(arr):
    item1 = arr[-2]
    item2 = arr[-1]
    rest = copy.deepcopy(arr[:-2])
    result = rest
    result.extend([item1[:-1], item1[-1] + item2])
    return result

def solution(arr):
    """
    Algorithm idea:
        greedy solution with recursion, check head and tail match or not, move combinations:
        move_head_left, move_head_right
        move_tail_left, move_tail_right
        if len(head) > len(tail) + 2:
            return False
        if len(head) = len(tail) + 2:  # head too long
            arr = move_head_right(arr)
            arr = move_tail_right(arr)
        if len(head) = len(tail) + 1:  # head too long
            arr = move_head_right(arr)
            # check

    edge case:
    len(arr) == 1: true
    len(arr) == 2:
        enumerate_possible_pair(arr[0], arr[1])
        is_pair_solution(arr[0], arr[1])
    len(arr) == 3:
        need to ensure middle item has enough char
    """
    if len(arr) <= 1:
        return True

    if len(arr) == 2:
        return is_pair_solution(arr[0], arr[1])

    head = arr[0]
    tail = arr[-1]
    if len(arr) == 3 and len(arr[1]) == 1:
        middle = arr[1]
        # handle cases
        if len(head) == len(tail) + 1:
            return head == middle + tail
        if len(head) == len(tail):
            return head == tail
        if len(head) + 1 == len(tail):
            return head + middle == tail
        return False
    
    # normal cases that middle can be borrowed by both head and tail
    if len(head) == len(tail) + 2:  # head too long
        head_right = move_head_right(arr)
        head_right_tail_right = move_tail_right(head_right)
        return solution(arr)

    if len(head) == len(tail) + 1:  # head too long
        head_right = move_head_right(arr)
        if solution(head_right) == True:
            return True
        # try move tail
        tail_right = move_tail_right(arr)
        return solution(tail_right)

    if len(head) == len(tail):
        if head == tail:
            trimmed_arr = arr[1:-1]
            return solution(trimmed_arr)
        
        # try both + 1
        head_left = move_head_left(arr)
        head_left_tail_right = move_tail_right(head_left)
        if head_left_tail_right[0] == head_left_tail_right[-1]:
            test = solution(head_left_tail_right[1:-1])
            if test == True:
                return True

        # try both - 1
        head_right = move_head_right(arr)
        head_right_tail_left = move_tail_left(head_right)
        if head_right_tail_left[0] == head_right_tail_left[-1]:
            test = solution(head_right_tail_left[1:-1])
            return test

        return False

    if len(head) + 1 == len(tail):  # head too short
        head_left = move_head_left(arr)
        if solution(head_left) == True:
            return True

        # try move tail
        tail_left = move_tail_left(arr)
        return solution(tail_left)

    if len(head) + 2 == len(tail):
        head_left = move_head_left(arr)
        head_left_tail_left = move_tail_left(arr)
        return solution(head_left_tail_left)

    return False


def test():
    assert is_pair_solution("ab", "cabc")
    assert is_pair_solution("abca", "bc")
    assert is_pair_solution("abca", "bcd") == False
    assert move_head_left(["a", "bc", "c"]) == ["ab", "c", "c"]
    assert move_head_right(["a", "bc", "c"]) == ["", "abc", "c"]
    assert move_tail_left(["a", "bc", "c"]) == ["a", "bcc", ""]
    assert move_tail_right(["a", "bc", "c"]) == ["a", "b", "cc"]
    print("passed test")


test()

arr_test = ["aa", "bab", "cde", "aba", "ab"]

print(solution(arr_test))

# execution time limit exceeded
failing_test = ["xxxx", 
 "xxxx", 
 "xxxx", 
 "xxxxxx", 
 "xx", 
 "xxxx"]