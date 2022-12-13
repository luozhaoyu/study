class Solution:
    """
    Algorithm:
    iterate thourgh the string
    1. if char is non-space: add to current_word
    2. if char is space:
      1. if current_word is empty: skip this
      2. if current_word is non-empty: add current_word to the head
    """
    def reverseWords(self, s: str) -> str:
        result = ""
        current_word = ""
        for c in s:
            if c == " ":
                if current_word:
                    result = current_word + " " + result
                    current_word = ""
            else:
                current_word += c
        if current_word:
            result = current_word + " " + result
            
        return result.rstrip()

s = Solution()
for test in (
    "the sky is blue",
    "  hello world  ",
    "a good   example",
):
    print(s.reverseWords(test))
