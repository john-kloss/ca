import numpy as np
import arff


class CFInnerNode(object):
    def __init__(self, t, b, d, metric, disMatrix, dataMatrix):
        self.childs = []
        self.isLeaf = False
        self.parent = None
        self.CF = CF(0,np.zeros(d),np.zeros(d))
        self.t = t
        self.b = b
        self.d = d  #dimension
        self.metric = metric
        self.isLeafNode = False
        self.centroid = 0
        self.diameter = 0
        self.maxDiameter = 0
        self.distanceMatrix = disMatrix
        self.dataMatrix = dataMatrix
        self.idList = []

    def addLeafNode(self,CFLeafNode):
        self.childs.append(CFLeafNode)
        self.idList.append(CFLeafNode.idList)
        CFLeafNode.parent = self
        self.update(CFLeafNode)
        if(len(self.childs) == self.b): #need to split
            self.split()

    def popChild(self,idx):
        popped_child = self.childs.pop(idx)
        self.idList.pop(idx)
        self.update(self)
        return popped_child

    def update(self, CFNode):
        self.CF = CF(0,np.zeros(self.d),np.zeros(self.d))
        for x in range(0, len(self.childs)):
            self.CF.add(self.childs[x].CF)

        self.centroid = np.divide(self.CF.ls,self.CF.N)

        if self.CF.N > 1 :
            self.diameter = self.distanceMatrix[list(flatten(self.idList))]

        if(self.parent != None) :
            self.parent.update(self),

    def split(self):
        index_farthest_points = farthest_points(self.childs,self.metric)
        index_p1 = min(index_farthest_points[0],index_farthest_points[1])
        index_p2 = max(index_farthest_points[0],index_farthest_points[1])
        #check if we have a parent or if we are the root

        if( self.parent is None ) :
            new_root = CFInnerNode(self.t,self.b,self.d,self.metric, self.distanceMatrix, self.dataMatrix)
            right_side = CFInnerNode(self.t, self.b, self.d,self.metric, self.distanceMatrix, self.dataMatrix)
            idxs_to_pop = []
            for x in range(len(self.childs)):   #decide where which child lands
                if x == index_p1:
                    continue
                if x == index_p2:
                    continue
                if(calculateDistance(self.childs[index_p2],self.childs[x],self.metric) <=  calculateDistance(self.childs[index_p1],self.childs[x],self.metric)):
                    #distance to p2 is smaller
                    idxs_to_pop.append(x)

            idxs_to_pop.append(index_p2)  # needed so that during the loop no elemts get removed, which would cause wrong indices
            idxs_to_pop.sort()
            already_popped = 0
            for x in range(len(idxs_to_pop)) :
                right_side.addLeafNode(self.popChild(idxs_to_pop[x] - already_popped))
                already_popped = already_popped + 1
            new_root.addLeafNode(self)
            new_root.addLeafNode(right_side)

        else:
            self.parent.addLeafNode(self.popChild(-1))

        return 0


def farthest_points(points, metric):
    x = y = 0
    maxDist= 0
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if i != j:
                dist = calculateDistance(points[i], points[j],metric)
                if dist > maxDist:
                    maxDist = dist
                    x = i
                    y = j
    return [x,y]

class CFLeafNode(object):
    def __init__(self,d,t,disMatrix,dataMatrix):
        self.data_ps = []
        self.CF = CF(0,np.zeros(d),np.zeros(d))
        self.isLeafNode = True
        self.parent = None
        self.d = d
        self.t = t
        self.distanceMatrix = disMatrix
        self.dataMatrix = dataMatrix
        self.idList = []
        self.diameter = 0

    def addData_p(self,data_p):
        # check if diameter would be too big
        self.idList.append(data_p.index)
        testdiameter = self.distanceMatrix[self.idList][:,self.idList].max()
        if testdiameter  > self.t:  # need create or add into another leave
            self.idList.pop(-1)
            newLeafNode = CFLeafNode(self.d, self.t, self.distanceMatrix, self.dataMatrix)
            newLeafNode.addData_p(data_p)
            self.parent.addLeafNode(newLeafNode)
        else:
            self.data_ps.append(data_p)
            data_p.parent = self
            self.update_CF()

    def update_CF(self):
        self.CF.N = self.CF.N + 1
        self.CF.ls = self.CF.ls + self.data_ps[-1].data
        self.CF.ss = self.CF.ss + self.data_ps[-1].data * self.data_ps[-1].data

        self.centroid = self.CF.ls * (1.0 / self.CF.N)

        if (self.CF.N > 1):
            self.diameter = self.distanceMatrix[self.idList][:,self.idList].max()

        if (self.parent != None):
            self.parent.update(self),

class data_p(object):
    def __init__(self,data, m_index):
        self.data = np.array(data)
        self.classLabel = 0
        self.isData = True
        self.parent = None
        self.centroid = np.array(data)  # for comparison
        self.index = m_index

class CF(object):
    def __init__(self,N,ls,ss):
        self.N = N
        self.ls = ls  # linear sum
        self.ss = ss  # square sum

    def add(self,other):
        self.N = self.N + other.N
        self.ls = self.ls + other.ls
        self.ss = self.ss + other.ss

    def sub(self,other):
        self.N = self.N - other.N
        self.ls = self.ls - other.ls
        self.ss = self.ss - other.ss



def calculateDistance(a, b, metric):
    if(metric == 'euclidian'):
        return np.linalg.norm(np.sqrt((a.centroid - b.centroid) * (a.centroid - b.centroid)))
    if(metric == 'seuclidan'):
        return  np.linalg.norm((a.centroid - b.centroid) * (a.centroid - b.centroid))
    if(metric == 'manhattan'):
        return np.linalg.norm(np.abs(a.centroid - b.centroid))
    return 0

# returns the nodes that identify a cluster
def parseTree(root, k):
    cluster = root.childs
    maxiter = 0
    while len(cluster) < k and maxiter < 50 :
        for x in range(0, len(cluster)): # for all nodes in the cluster
            if not cluster[x].isLeafNode and (len(cluster) + 1) < k : # if it's not a leaf remove it and add it's leaves
                for y in range(0,len(cluster[x].childs)):
                    cluster.append(cluster[x].childs[y])
                cluster.remove(cluster[x])
                break
        maxiter = maxiter + 1
    cluster = cluster[:k]
    # we've got the nodes that identify the cluster, now find all the leaves in the cluster
    # or add just the new indices ;)
    for x in range(0, len(cluster)):
        cluster[x] = list(flatten(cluster[x].idList))

    return cluster


def getLabels(cluster, nodes):

    for x in range(0, len(nodes)):
        found = False
        for y in range(0, len(cluster)):
                if nodes[x] in cluster[y]:
                        found = True
                        print y
                        break
        if not found:
            print len(cluster) + 1


def createDistanceMatrix(data,metric):
    distanceMatrix = np.zeros(shape=(len(data),len(data)))
    for x in range(0,len(data)):
        for y in range(0, len(data)):
            distanceMatrix[x][y] = calculateDistance(data[x],data[y],metric)

    return distanceMatrix;


def flatten(L):
    for item in L:
        if isinstance(item, list):
            for subitem in item:
                yield subitem
        else:
            yield item

def birch(path, threshold, b, cluster, metric):

    # building a CF-tree
    # start with a node which we call root
    file1 = open(path, "rb")
    dataset = arff.load(file1)

    data = np.array([x[:-1] for x in dataset['data']])

    # creating data points from rows
    data_points = [0 for i in range(len(data))]
    for x in range(0, len(data)):
        data_points[x] = data_p(data[x],x)

    distanceMatrix = createDistanceMatrix(data_points, metric)

    root = CFInnerNode(threshold, b, len(data[0]), metric, distanceMatrix, data)
    # add first node by hand
    leaf_node = CFLeafNode(len(data[0]),threshold, distanceMatrix,data)
    leaf_node.addData_p(data_points[0])

    root.addLeafNode(leaf_node)

    for x in range(1, len(data)):
        newEntry = data_points[x]
    # 1. Identifying the appropriate leaf
        # identify root new if needed
        while(root.parent is not None):
            root = root.parent
        node = root
        while True:
            minDist = 999999999
            closest = None
            for y in range(0, len(node.childs)):  # calculate distances to node entries
                dist = calculateDistance(newEntry, node.childs[y],metric)
                if dist < minDist:
                    minDist = dist
                    closest = y
            if node.childs[closest].isLeafNode: # we are at a leaf
                distance = minDist
                parent = node.childs[closest].parent
                break
            node = node.childs[closest]

        # 2. Modifying the leaf   merge then check for threshold condition
        # Would a merge violate the threshold  condition?
        node.childs[closest].addData_p(newEntry)

    while (root.parent is not None):
        root = root.parent


    #parse tree from root and receive k cluster
    cluster = parseTree(root,cluster)
    nodes_idxs = [i for i in range(len(data))]
    getLabels(cluster, nodes_idxs)


birch('./data/' + 'c_Moons1' + '.arff',2, 1500, 2,'euclidian')