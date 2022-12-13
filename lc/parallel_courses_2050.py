from typing import List

class Solution:
    """
    Algorithm:
    loop:
        1. update current node's upstreams
        2. find upstream dependencies without downstreams
        3. put dependencies into queue
    """
    def update_node(self, node):
        for up in self.upstream.get(node, []):
            if up in self.min_time:  # up time is set
                self.min_time[up] = max(self.min_time[up], self.min_time[node] + self.time[up-1]) 
            else:
                self.min_time[up] = self.min_time[node] + self.time[up-1]

    def remove_node(self, node):
        # find all upstreams
        upstreams = self.upstream.get(node)
        if upstreams:
            # delete relation
            for up in upstreams:
                self.downstream[up].remove(node)

        if node in self.downstream:
            del self.downstream[node]
        if node in self.upstream:
            del self.upstream[node]

    def find_next_nodes(self):
        result = []
        # delete relation
        for node in self.downstream:
            # filter out no downstream nodes
            if len(self.downstream.get(node)) <= 0:  # it is empty
                result.append(node)
        return result

    def build_dependency(self, relations):
        for i in range(1, len(self.time)+1):
            self.downstream[i] = set()
            self.upstream[i] = set()

        for relation in relations:
            up, down = relation[0], relation[1]
            if down in self.upstream:
                self.upstream[down].add(up)
            else:
                self.upstream[down] = set([up])

            if up in self.downstream:
                self.downstream[up].add(down)
            else:
                self.downstream[up] = set([down])

    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        self.time = time
        self.upstream, self.downstream = {}, {}
        self.build_dependency(relations)
        print(self.upstream, self.downstream)

        self.min_time = {}
        # key is node, value is minimumTime
        for i in range(len(time)):
            self.min_time[i+1] = self.time[i]

        queue = self.find_next_nodes()
        while queue:
            current_node = queue.pop(0)
            self.update_node(current_node)

            self.remove_node(current_node)

            # find upstream without downstream
            nodes = self.find_next_nodes()
            # print("queue=", queue, current_node, nodes)
            queue.extend(nodes)
        return max(self.min_time.values())
        

s = Solution()
for n, relations, time in (
        (3, [[1,3],[2,3]], [3,2,5]),
        (5,[[1,5],[2,5],[3,5],[3,4],[4,5]],[1,2,3,4,5]),
        (2,[[2,1]], [10000, 10000]),
):
    print(s.minimumTime(n, relations, time))
