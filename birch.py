import numpy as np
import math


class Tree(object):
    def __init__(self):
        self.children = []
        self.pos = None
        self.data = []


def printTree(tree):
    for x in range(0, len(tree.children)):
        print tree.children[x].data


def calculateDistance1(a, b):
    distance = 0
    for x in range(0, len(a)):
        distance = distance + math.sqrt(a[x, x] ** 2 + b[x] ** 2)
    return distance

def calculateDistance2(a, b):
    distance = 0
    for x in range(0, len(a)):
        distance = distance + math.sqrt(a[x,x] ** 2 + b[x,x] ** 2)
    return distance


# calculate the average position of a node
def posTree(tree):
    pos = []
    #for all dimension
    for x in range(0, tree.data[0].shape[1]-1):
        count = 0
        #for all data points
        for y in range(0, len(tree.data)):
            count = count + tree.data[y][0,x]
        pos.append(count/len(tree.data))
    return pos


def birch(data, t, b):
    root = Tree()
    root.data = "root"

    # building a CF-tree

    # init with first item
    root.children.append(Tree())
    root.children[0].data.append(data[0, ])

    # sort all elements into tree based on distance
    for x in range(1,data.shape[0]):
        newNode = data[x, ]
        # 1. Identifying the appropriate leaf
        node = root
        while len(node.children) != 0:
            minDist = 1000
            closest = None
            for x in range(0, len(node.children)):
                if calculateDistance1(newNode, posTree(node.children[x])) < minDist:
                    minDist = calculateDistance1(newNode, posTree(node.children[x]))
                    closest = x
            node = node.children[closest]

        # Find the closest leaf entry
        minDist = 1000
        closest = None
        for x in range(0, len(node.data)):
            if calculateDistance2(newNode, node.data[x]) < minDist:
                minDist = calculateDistance2(newNode, node.data[x])
                closest = x

        # 2. Modifying the leaf

        # Would a merge violate the threshold  condition?
        if minDist < t:
            print 'no violation'
            # Would a merge violate the branching factor?
            if len(node.data) < b:
                print 'add node'
                node.data.append(newNode)
                print node.data
            else:
                print 'split'
        else:
            print 'violation'



        # 3. Modifying the path to the leaf


        # return list_of_labels


birch(np.matrix('5.1 3.5 1.4 0.2 0;4.7 3.2 1.3 0.2 0;5 3.6 1.4 0.2 0;4.6 3.4 1.4 0.3 0'), 10, 5)
