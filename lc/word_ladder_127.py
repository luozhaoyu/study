from typing import List
import copy

class Word:
    def __init__(self, word, count=0, precursor=None):
        self.word = word
        self.count = count
        self.precursor = precursor
        if not precursor:
            self.precursor = []

class Solution:
    def is_adjacent(self, word_a, word_b) -> bool:
        diffs = 0
        i, j = 0, 0
        while i < len(word_a) and j < len(word_b):
            if word_a[i] != word_b[j]:
                diffs += 1
                if diffs > 1:
                    return False
            i += 1
            j += 1

        diffs += len(word_a) - i + len(word_b) - j
        if diffs > 1:
            return False
        return True


    def append_to_dict(self, key, value, input_dict):
        if key in input_dict:
            input_dict[key].append(value)
        else:
            input_dict[key] = [value]

    def find_non_visited_adjacents(self, current_word):
        non_visited = set(self.adjacents[current_word.word]) - self.visited
        result = []
        for word in non_visited:
            precursor = copy.copy(current_word.precursor)
            precursor.append(current_word.word)
            result.append(Word(word, count=current_word.count + 1, precursor=precursor))
        return result

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # key is word, value is adjacent list
        self.adjacents = {}
        wordList.extend([beginWord])
        for i in range(len(wordList)):
            for j in range(i+1, len(wordList)):
                if self.is_adjacent(wordList[i], wordList[j]):
                    self.append_to_dict(wordList[i], wordList[j], self.adjacents)
                    self.append_to_dict(wordList[j], wordList[i], self.adjacents)
        # print(self.adjacents)

        self.visited = set()

        queue = [Word(beginWord)]

        # queue is not empty
        while queue:
            # pop the first item
            current_word = queue.pop(0)

            self.visited.add(current_word.word)

            # find item's non-visited adjacents, append to queue
            non_visited_adjacents = self.find_non_visited_adjacents(current_word)

            # return directly if found
            for word in non_visited_adjacents:
                if word.word == endWord:
                    print(word.precursor)
                    return word.count + 1
                queue.append(word)
        return 0
        

s = Solution()
s.ladderLength("hit", "cog", ["hot","dot","dog","lot","log"])
        
