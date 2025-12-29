import re
from typing import List


class Solution:
    """
    Attributes:
        savedName = {
            "onepiece": maxK
        }
    """
    savedName = {}
    result = []
    exists = set()

    def saveNewName(self, name, k=0):
        """
        we should save the name and its suffix to speed up lookup
        """
        finalName = self.generateNameWithSuffix(name, k)
        self.savedName[name] = k
        self.result.append(finalName)
        self.exists.add(finalName)

    def generateNameWithSuffix(self, name, k):
        if k == 0:
            return name
        return f"{name}({k})"

    def findNewName(self, name):
        k = self.savedName.get(name, 0)
        k += 1
        while True:
            newName = self.generateNameWithSuffix(name, k)
            # it can conflict with the name that has same prefix
            if newName in self.exists:
                k += 1
                continue
            return name, k

    def getFolderNames(self, names: List[str]) -> List[str]:
        """
        1. check folder name already exists?
        - if not, save the name
        2. find next folder name with (current_name, k)
        - if name exists, bump k += 1
        3. save the right name
        """
        self.result = []
        self.savedName = {}
        self.exists = set()

        for name in names:
            # print("getFolderNames:", name, self.savedName, self.result)
            if name not in self.exists:
                self.saveNewName(name)
                continue

            parsedName, k = self.findNewName(name)
            self.saveNewName(parsedName, k)
        return self.result


test = ["kaido","kaido(1)","kaido","kaido(1)"]
expected = ["kaido","kaido(1)","kaido(2)","kaido(1)(1)"]
s = Solution()
result = s.getFolderNames(test)
print(result == expected, result)