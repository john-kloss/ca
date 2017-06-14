import numpy as np
import math


class CFNode(object):
    def __init__(self, CFEntry):
        self.entries = [CFEntry]  # contains CFEntries
        self.isLeaf = True

    def findFarthestEntries(self):
        x = y = 0
        maxDist = 0
        for i in range(0,len(self.entries)):
            for j in range(0, len(self.entries)):
                if i != j:
                    dist = calculateDistance(self.entries[i], self.entries[j])
                    if dist > maxDist:
                        maxDist = dist
                        x = i
                        y = j
        return [self.entries[x], self.entries[y]]


class CFEntry(object):
    def __init__(self, pos):
        self.child = None  # link to next CFNode
        self.count = 1
        self.ls = pos  # linear sum
        self.ss = pos  # square sum

    def update(self, newEntry):
        # self.count = self.count+1
        # for each dimension
        for x in range(0, self.ls.shape[1] - 1):
            self.ls[0,x] = (self.ls[0,x] * self.count + newEntry.ls[0,x]) / (self.count+1)
        self.count += self.count


def calculateDistance(a, b):
    distance = 0
    for x in range(0, a.ls.shape[1]-1):
        s = math.sqrt((a.ls[0, x] - b.ls[x]) ** 2)
        distance = distance + s
    return distance


def getListOfLabels(root, data):
    node = root
    listOfLabels = []
    for x in range(0, data.shape[0]):
        while True:
            minDist = 1000
            closest = None
            for y in range(0, len(node.entries)):  # calculate distances to node entries
                dist = calculateDistance(CFEntry(data[x, ]), node.entries[y])
                if dist < minDist:
                    minDist = dist
                    closest = y
            if node.entries[closest].child is None:
                listOfLabels.append(node.entries[closest].ls)
                break
            node = node.entries[closest].child

    print listOfLabels
    return listOfLabels



def birch(data, t, b):
    # building a CF-tree
    # init with first item
    root = CFNode(CFEntry(data[0, ]))
    root = CFNode(None)
    root.isLeaf = False
    root.entries = [CFEntry([1,1,1,1]), CFEntry([2,2,2,2])]
    return getListOfLabels(root, data)

    # sort all elements into tree based on distance
    for x in range(1, data.shape[0]):
        newEntry = CFEntry(data[x,])
    # 1. Identifying the appropriate leaf
        node = root
        closestLeafEntry = None
        distance = 0
        while True:
            minDist = 1000
            closest = None
            for y in range(0, len(node.entries)):  # calculate distances to node entries
                dist = calculateDistance(newEntry, node.entries[y])
                if dist < minDist:
                    minDist = dist
                    closest = y
            if node.entries[closest].child is None:
                closestLeafEntry = node.entries[closest]
                distance = minDist
                break
            node = node.entries[closest].child
        # 2. Modifying the leaf
        # Would a merge violate the threshold  condition?
        if distance < t:
            print 'no violation'
            # Update the CF entry for the leaf
            closestLeafEntry.update(newEntry)

        else:
            print 'violation'
            # Add a new entry
            node.entries.append(newEntry)
            # Does the merge violate the branching factor?
            if len(node.entries) >= b:
                print 'split'
                # Find the two farthest point
                farthestPoints = node.findFarthestEntries()
                # Insert non-leaf entry into the parent node






    # return list_of_labels


birch(np.matrix('5.1 3.5 1.4 0.2 0;4.7 3.2 1.3 0.2 0;5 3.6 1.4 0.2 0;4.6 3.4 1.4 0.3 0'), 2.8, 1)
