import numpy as np

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

def birch(data, t, b):
    root = Tree()
    root.data = "root"

    #building a CF-tree
    root.left = Tree()
    root.left.data = data[0,]
    root.right = Tree()
    root.right.data = data[1,]
    print root.left.data

birch(np.matrix('5.1 3.5 1.4 0.2 0;4.7 3.2 1.3 0.2 0;5 3.6 1.4 0.2 0;4.6 3.4 1.4 0.3 0'),1,1)
