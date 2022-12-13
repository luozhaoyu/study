from typing import List

class Solution:
    """
    words = ["i","love","leetcode","i","love","coding"], k = 2
    -> ("i", 2) ("love", 2) -> find top k most frequent
    1. random pick value x, loop through n items -> x <= a items
    2. if a == k, return the list
       if a < k, return the list, keep find k - a -> k = k - a
       if a > k, check on the large list
    """
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        word_dict = {}
        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

        # convert the dict in list of tuple: [("i", 2)]
        word_counts = [(key, word_dict[key]) for key in word_dict]

        result_tuples = self.find_top_k(word_counts, k)
        result_sorted = sorted([i for i in result_tuples], key=lambda x: (-x[1], x[0]))
        return [i[0] for i in result_sorted]

    def find_top_k(self, word_counts, k: int):
        # return directly if k is more than current list size
        if len(word_counts) <= k:
            return word_counts

        # set baseline value x
        x = word_counts[0][1]

        # large_words is the word tuple larger than baseline value
        large_words = []
        small_words = []
        len_equal = 0
        for i in word_counts:
            if i[1] > x:
                large_words.append(i)
            elif i[1] < x:
                small_words.append(i)
            else:
                if i[0] < word_counts[0][0]:
                    large_words.append(i)
                elif i[0] > word_counts[0][0]:
                    small_words.append(i)
                else:
                    len_equal += 1

        len_large = len(large_words)
        len_small = len(small_words)

        """
        1. k <= len_large
        2. k <= len_large + len_equal
        3. k > len_large + len_equal 
        """

        if k <= len_large:  # only need to find in the large sets
            return self.find_top_k(large_words, k)

        large_words.append(word_counts[0])
        if k <= len_large + len_equal:  # some are equal words
            return large_words

        large_words.extend(self.find_top_k(small_words, k - len_large - len_equal))
        return large_words
        

s = Solution()
words = ["i","love","leetcode","i","love","coding"]
words = ["the","day","is","sunny","the","the","the","sunny","is","is"]
print(s.topKFrequent(words, 4))
