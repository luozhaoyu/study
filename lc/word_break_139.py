from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        print(s)
        if not s:
            return True
        temp = ""
        i = 0
        while i < len(s):
            temp += s[i]
            if temp in wordDict:  # break here or continue
                if self.wordBreak(s[i+1:], wordDict):
                    return True
            i += 1
        return False

s = Solution()
for string, wordDict in (
        ("leetcode", ["leet","code"]),
        ("applepenapple", ["apple","pen"]),
        ("catsandog", ["cats","dog","sand","and","cat"]),
        ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
         ["a","aa","aaa","aaaa","aaaaa","aaaaaa","aaaaaaa","aaaaaaaa","aaaaaaaaa","aaaaaaaaaa"]),
):
    print(s.wordBreak(string, wordDict))
