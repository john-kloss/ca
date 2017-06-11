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
                    print i,j
                    #calculateDistance(self.entries[i], self.entries[j])
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
        print x
        # distance = distance + math.sqrt(a.ls[0, x] ** 2 + b[0, x] ** 2)
    return distance / a.ls.shape[1]



def birch(data, t, b):

    # building a CF-tree
    # init with first item
    root = CFNode(CFEntry(data[0, ]))

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
                if calculateDistance(newEntry, node.entries[y].ls) < minDist:
                    minDist = calculateDistance(newEntry, node.entries[y].ls)
                    closest = y
            if node.entries[closest].child is None:
                closestLeafEntry = node.entries[closest]
                distance = minDist
                break
            node = node.entries[closest]
        print distance
        # 2. Modifying the leaf
        # Would a merge violate the threshold  condition?
        if distance < t:
            print 'no violation'
            # Update the CF entry for the leaf
            closestLeafEntry.update(newEntry)

        else:
            print 'violation'
            # Add a new entry
            node.entries.append(CFEntry(newEntry))
            # Does the merge violate the branching factor?
            if len(node.entries) >= b:
                print 'split'
                # Find the two farthest point
                node.findFarthestEntries()




                # 3. Modifying the path to the leaf


                # return list_of_labels


birch(np.matrix('5.1 3.5 1.4 0.2 0;4.7 3.2 1.3 0.2 0;5 3.6 1.4 0.2 0;4.6 3.4 1.4 0.3 0'), 2.8, 1)
