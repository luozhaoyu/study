"""
You have a positive integer n. Return the smallest possible number m that is:

Greater than n;
An even number;
The digits of which are permutation of n's digits.
If such an m doesn't exist, return -1.

Example

For n = 1147, the output should be
solution(n) = 1174.
"""

def solution(n):
    """
    Algorithm:
        Simulate how human-being do this operation:
        1. popping digits one by one until current digit can bump to next larger digit
        2. swap current digit with next larger digit
        3. append the popped digit
            1. sort them first
            2. find the first even number, then move it to the end

    Data Structure:
        1. use a stack to store current position
        2. use a set to store popped_digits
    """
    current = []
    i = n
    while i:
        current.insert(0, i % 10)
        i = int(i / 10)


    next_number = find_next_number(current)
    while next_number:
        # print(next_number)
        if next_number[-1] % 2 == 0:  # right answer
            return int("".join([str(i) for i in next_number]))
        next_number = find_next_number(next_number)
    return -1


def has_even_number(digits):
    for i in digits:
        if i % 2 == 0:
            return True
    return False


def find_next_number(current):
    # popping digits rules:
    # 1. if popped_digits is empty, then pop
    # 2. if current index can swap with next bigger number
    # 3. if popped_digits doesn't have even number
    popped_digits = []
    while current:
        # print(current, popped_digits)
        if not popped_digits:
            i = current.pop()
            popped_digits.append(i)
            continue

        # if not has_even_number(popped_digits):
        #     i = current.pop()
        #     popped_digits.append(i)
        #     continue

        # swap
        if try_swap_larger_digit(popped_digits, current):  # swap succeed
            # append the remaining digits
            popped_digits.sort()

            # print("swapped: ", current, popped_digits)
            found_even_number = False
            # handle the even number
            for i in range(len(popped_digits))[::-1]:
                if popped_digits[i] % 2 == 0:
                    found_even_number = True
                    temp = popped_digits[i]
                    popped_digits.pop(i)
                    popped_digits.append(temp)
                    break

            if found_even_number:
                current.extend(popped_digits)
                return current
            else:
                continue
        else:  # failed: no larger
            i = current.pop()
            popped_digits.append(i)
            continue
    return False


def try_swap_larger_digit(popped_digits, current_list):
    """
    Returns:
        True, when found larger digit in popped_digits compared with current_list[-1]
    """
    popped_digits.sort()
    for i in range(len(popped_digits)):
        if popped_digits[i] > current_list[-1]:  # found one, then swap
            popped_digits[i], current_list[-1] = current_list[-1], popped_digits[i]
            return True
    return False



print(solution(1147))
print(solution(1147321))
print(solution(1147222238))
print(solution(743108996))
print(solution(404133759135975))

