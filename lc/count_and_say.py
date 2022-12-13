class Solution:
    def countAndSay(self, n: int) -> str:
        tmp = "1"
        for i in range(n-1):
            new_tmp = ""
            j = 0
            # find continuous digit
            while j < len(tmp):
                letter = tmp[j]
                count = 1
                while j + 1 < len(tmp) and tmp[j] == tmp[j+1]:
                    count += 1
                    j += 1
                # find repeating letters, add to new_tmp
                new_tmp += str(count) + letter
                j += 1
            tmp = new_tmp
        return tmp

s = Solution()
s.countAndSay(1)
            
