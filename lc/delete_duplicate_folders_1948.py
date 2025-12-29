from typing import List


class Node:
    """
    Attributes:
        child = set(node1, node2)
    """
    def __init__(self, value):
        self.value = value
        self.child = {}
        self.digest = None

    def addChild(self, node):
        self.child[node.value] = node

    def __repr__(self):
        return f"({self.value}, {self.digest}, {self.child})"


class Solution:
    """
    Attributes:
        nodeContent: stores the digest of the node content to determine if
    two nodes share the same content
        nodeContent = {
            "digest1": set(node1, node2)
            "y": set("/x/y", "/w/y")
        }
    """
    nodeContent = {}
    result = set()
    globalDigest = {}

    def insertPath(self, path, node):
        """
        path = ["a", "b"]
        go through each value, if current value is not in current node child, then create a new node as child and keep going
        """
        current_node = node
        for value in path:
            if value in current_node.child:
                current_node = current_node.child[value]
                continue
            # child doesn't have this value, so need to create a new Node
            newNode = Node(value)
            current_node.addChild(newNode)
            current_node = newNode

    def constructTRIE(self, paths: List[List[str]]) -> Node:
        """
        1. save all paths into result
        2. construct the tree
        """
        root = Node("/")
        for path in paths:
            self.result.add(tuple(path))
            self.insertPath(path, root)
        return root

    def digest(self, content: List[str]) -> str:
        content.sort()
        return ",".join(content)

    def addToDigestDB(self, digest):
        if digest in self.globalDigest:
            self.globalDigest[digest] += 1
        else:
            self.globalDigest[digest] = 1

    def traverseNodeAndGetDigest(self, node):
        """
        currentNodeDigest = digest(order(childNodeDigest))

        if no child, then value itself is the digest
        """
        if not node.child:  # it is not a folder, so it doesn't have digest
            node.digest = ""
            return node.digest

        allDigest = []
        for child in node.child.values():
            childDigest = self.traverseNodeAndGetDigest(child)
            if not childDigest:  # the child is not a folder, it is a file
                childDigest = child.value
            else:
                childDigest = child.value + "/" + childDigest
            allDigest.append(childDigest)

        node.digest = self.digest(allDigest)
        self.addToDigestDB(node.digest)
        return node.digest

    def getFinalMatchNode(self, path, node):
        current_node = node
        for value in path:
            if value in current_node.child:  # child has this value, continue proceeding
                current_node = current_node.child[value]
            else:  # no match return this node and unmatched value
                return current_node, value
        # arriving at last node, match successfully
        return current_node, None
            

    def getPathDigest(self, path, node):
        finalNode, value = self.getFinalMatchNode(path, node)
        if value == None:  # match successfully
            return finalNode.digest
        # match failed
        raise Exception(f"it shouldn't have unmatched value: {node} for {path}")

    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        """
        0. save the input as temporary result
        1. input is a list, construct a TRIE tree: without tree, we couldn't
        get the full content under a node
        2. need to traverse the whole tree to get each node content digest
        3. go through digest result, remove them from result if set size > 1
        """
        self.result = set()
        self.globalDigest = {}
        root = self.constructTRIE(paths)
        self.traverseNodeAndGetDigest(root)

        print(root)
        print(self.globalDigest)

        result = []
        for path in paths:
            digest = self.getPathDigest(path, root)
            if not digest:  # it is a file, so add to result
                result.append(path)
                continue
            if self.globalDigest.get(digest, -1) <= 1:  # no duplication
                result.append(path)
        print(result)
        return result

        self.deleteBasedOnDuplicatedDigest()
        return self.result
        
paths = [["a"],["c"],["a","b"],["c","b"],["a","b","x"],["a","b","x","y"],["w"],["w","y"]]
paths = [["a"],["c"],["d"],["a","b"],["c","b"],["d","a"]]
#paths = [["a","b"],["c","d"],["c"],["a"]]
#paths = [["a"],["a","x"],["a","x","y"],["a","z"],["b"],["b","x"],["b","x","y"],["b","z"],["b","w"]]
s = Solution()
s.deleteDuplicateFolder(paths)