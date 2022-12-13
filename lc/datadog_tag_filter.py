class Solution:
    def __init__(self, l):
        self.data = {}
        for line in l:
            tags = [t.strip() for t in line.split(",")]
            for tag in tags:
                connects = set(tags)
                connects.remove(tag)
                if tag in self.data:
                    self.data[tag].union(connects)
                else:
                    self.data[tag] = connects
        print(self.data)

    def filter_by(self, l):
        result = self.data[l[0]]
        for filter_str in l[1:]:
            result = result.intersection(self.data[filter_str])
        return result

    def check_compression(self, s, compress):
        """
        iterate through compress, if char is letter, then check corresponding s[i]
        else: move i behind
        """
        i = 0
        j = 0
        while i < len(s) and j < len(compress):
            if compress[j].isalpha():
                if compress[j] == s[i]:
                    j += 1
                    i += 1
                    continue
                else:
                    return False
            else:
                i += int(compress[j])
                j += 1
                continue
        if i == len(s) and j == len(compress):
            return True
        return False
        

l = ['apple, facebook, google', 'banana, facebook', 'facebook, google, tesla', 'intuit, google, facebook']
s = Solution(l)
s.filter_by(["apple", "google"])
s.check_compression("datadog", "7")
