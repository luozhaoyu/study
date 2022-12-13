from typing import List

class Solution:
    """
    Algorithm:
      store dependency, find the minimum degree, update degree
    1. keep each node's dependency 
    2. find node without dependency, put it to answer, remove node has it as dependency
    3. go to 2 until exhausted

    Attributes:
      dependency: key: node value, value: set of value indicate who is upstream dependency
    """
    def __init__(self):
        self.dependency = {}

    def build_dependeny(self, numCourses, prerequisites):
        # initialize each node has no dependency
        for i in range(numCourses):
            self.dependency[i] = set()

        for dependency in prerequisites:
            course, prerequisite = dependency
            if course in self.dependency:
                self.dependency[course].add(prerequisite)
            else:
                self.dependency[course] = set(prerequisite)

    def find_zero_dependency_node(self):
        for course in self.dependency:
            # find empty dependency course
            if len(self.dependency[course]) == 0:
                # print(course, self.dependency)
                return course
        # can't find next couse without dependency
        return None

    def remove_node(self, node):
        for course in self.dependency:
            self.dependency[course].discard(node)
        del self.dependency[node]
        
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        self.build_dependeny(numCourses, prerequisites)

        # print(self.dependency)
        result = []
        # keep finding next zero dependency
        next_node = self.find_zero_dependency_node()
        while next_node != None:
            result.append(next_node)
            self.remove_node(next_node)
            next_node = self.find_zero_dependency_node()

        if len(result) == numCourses:
            return result
        return []
        
s = Solution()
s.findOrder(2, [[1,0]])
