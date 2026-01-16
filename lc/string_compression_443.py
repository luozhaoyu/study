class Solution:
    def compress(self, chars: List[str]) -> int:
        """
        use a stack to pop in one by one
        1. check if it is a new char
            yes: pop existing thing into stack
            no: increase count
        """
        result = []

        previous_char = chars[0]

        i = 1
        count = 1
        while i < len(chars):
            # print(chars)
            char = chars[i]
            if char == previous_char:  # same char
                count += 1
                chars.pop(i)
            else:  # new char
                # pop existing into result
                previous_char = char

                # pop the count
                # no need to pop count == 1
                if count == 1:
                    i += 1
                    continue

                count_str = str(count)
                for count_char in count_str:
                    chars.insert(i, count_char)
                    i += 1

                # start new count
                count = 1
                i += 1

        # chars.append(previous_char)

        if count > 1:
            count_str = str(count)
            for count_char in count_str:
                chars.append(count_char)


        return len(chars)
        