"""
s = "catsandog"
wordDict = ["cats","dog","sand","and","cat"]


catsandog
000100101
001010101 -> save state -> (previous_word_indexs, cursor)
001001000
previous_word_indexs = [2, 5, 12]
cursor = [15]
current_chars = s[previous_word_indexs[:-1], cursor]
"""

class CurrentState:
    def __init__(self, previous_word_indexs: List[int], cursor):
        self.previous_word_indexs = previous_word_indexs
        self.cursor = cursor

    def get_current_chars(self, s):
        return s[self.previous_word_indexs[-1], self.cursor]

    def rewind(self):
        previous_word_indexs = previous_word_indexs[:-1].append(previous_word_indexs[-1] + 1)


class Solution:
    def workBread(self, s: str, wordDict: List[str]) -> List[str]:
        self.s = s
        self.wordDict = wordDict

    def solution_exhaustion(self):
        res = set()
        current_state = CurrentState([0], 0)
        while current_state is not None:
            if self.is_current_state_ok(current_state):
                res.add(self.current_state)
            current_state = self.get_next_state(current_state)

    def is_cursor_exceed(self, cursor):
        return cursor >= len(self.s)

    def get_next_state(self, current_state):
        """return next_state or None"""
        # advance cursor by 1
        current_state.cursor += 1

        previous_word_indexs = current_state.previous_word_indexs
        # exit condition: current_state goes to the end, and previous_word_indexs is empty
        if self.is_cursor_exceed(current_state.cursor) and not previous_word_indexs:
            return None

        # exceed the end of string
        # tear down the previous word, reset cursor to the last word index
        if self.is_cursor_exceed(current_state.cursor):
            current_state.rewind()
            return self.get_next_state(current_state)


        # find next valid word
        # if can't find, then backtrack again
        current_word = current_state.get_current_chars()
        if current_word in self.wordDict:
            current_state.previous_word_indexs.append(cursor)
            # when cursor goes to the end, then return
            if cursor == len(self.s) - 1:
                return current_state
        else:
            return self.get_next_state(current_state)
