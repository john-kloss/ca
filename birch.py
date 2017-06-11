import numpy as np
import math

class CFNode(object):
    def __init__(self, CFEntry):
        self.entries = [CFEntry]  # contains CFEntries
        self.isLeaf = True


class CFEntry(object):
    def __init__(self, pos):
        self.child = None  # link to next CFNode
        self.count = 1
        self.ls = pos  # linear sum
        self.ss = pos  # square sum


def printTree(tree):
    for x in range(0, len(tree.children)):
        print tree.children[x].data

def calculateDistance(a, b):
    distance = 0
    for x in range(0, len(a)):
        distance = distance + math.sqrt(a[x, x] ** 2 + b[x, x] ** 2)
    return distance


# calculate the average position of a tree
def posTree(tree):
    pos = []
    # for all dimension
    for x in range(0, tree.data[0].shape[1] - 1):
        count = 0
        # for all data points
        for y in range(0, len(tree.data)):
            count = count + tree.data[y][0, x]
        pos.append(count / len(tree.data))
    return pos


def birch(data, t, b):

    # building a CF-tree
    # init with first item
    root = CFNode(CFEntry(data[0, ]))

    # sort all elements into tree based on distance
    for x in range(1, data.shape[0]):
        newEntry = data[x,]
    # 1. Identifying the appropriate leaf
        node = root
        closestLeaf = None
        distance = 0
        while True:
            minDist = 1000
            closest = None
            for y in range(0, len(node.entries)):  # calculate distances to node entries
                if calculateDistance(newEntry, node.entries[y].ls) < minDist:
                    minDist = calculateDistance(newEntry, node.entries[y].ls)
                    closest = y
            if node.entries[closest].child is None:
                closestLeaf = node.entries[closest]
                distance = minDist
                break
            node = node.entries[closest]

        # 2. Modifying the leaf

        # Would a merge violate the threshold  condition?
        if distance < t:
            print 'no violation'
            # Update the CF entry for the leaf
            closestLeaf.count = closestLeaf.count + 1

        else:
            print 'violation'
            # Would a merge violate the branching factor?
            if len(node.entries) < b:
                print 'add node'
            else:
                print 'split'



                # 3. Modifying the path to the leaf


                # return list_of_labels


birch(np.matrix('5.1 3.5 1.4 0.2 0;4.7 3.2 1.3 0.2 0;5 3.6 1.4 0.2 0;4.6 3.4 1.4 0.3 0'), 10, 5)
