"""
For

code1 = ["def is_even_sum(a, b):",
         "    return (a + b) % 2 == 0"]
and

code2 = ["def is_even_sum(summand_1, summand_2):",
         "    return (summand_1 + summand_2) % 2 == 0"]
the output should be solution(code1, code2) = true.
"""

def parse_definition(definition_str):
    """
    1. extract the params
    2. assign each param
    """
    temp = definition_str.split("(")
    if len(temp) < 2:
        print("error, didn't find param definition")
        return {}

    after_first_left_bracket = temp[1]
    temp = after_first_left_bracket.split(")")
    if len(temp) < 2:
        print("error, didn't find param definition")
        return {}
    before_right_bracket = temp[0]

    params = before_right_bracket.split(",")
    result = {}
    i = 0
    for param in params:
        trimmed = param.strip()
        result[trimmed] = f"p{i}"
        i += 1
    return result
    


def hash_function(line, hash_map):
    """
    1. parse function param, then store it
    2. go through each token, replace them if found match in store

    Data structure:
    hashed_params = {
        "symbol": "p1",
        "symbol2": "p2",
    }
    """
    i = 0
    result = ""
    # check each character, try to find token which starts with alphabet
    while i < len(line):
        # skip empty string
        if line[i] == " ":
            i += 1
            continue

        if line[i].isalpha():  # start to extract this token
            token = line[i]
            while i+1 < len(line) and (line[i+1].isalnum() or line[i+1] == "_"):
                token += line[i+1]
                i += 1
            # finish extract token
            if token in hash_map:
                result += hash_map[token]
            else:
                result += token
        else:  # if not start with alpha, then it couldn't be param
            result += line[i]
        i += 1
    return result

def solution(code1, code2):
    if len(code1) != len(code2):
        return False

    code1_hash_map = parse_definition(code1[0])
    code2_hash_map = parse_definition(code2[0])
    # print(code1_hash_map, code2_hash_map)

    i = 1
    while i < len(code1):
        hashed_code1 = hash_function(code1[i], code1_hash_map)
        hashed_code2 = hash_function(code2[i], code2_hash_map)
        # print(hashed_code1, hashed_code2)
        if hashed_code1 != hashed_code2:
            return False
        i += 1
    return True


def test():
    code1 = ["def foo(a, b):",
         "    return a + a"]
    code2 = ["def foo(b, a):",
         "    return b + b"]
    print(solution(code1, code2))


test()