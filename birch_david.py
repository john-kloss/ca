import numpy as np
import arff

class CFInnerNode(object):
    def __init__(self, t, b, d):
        self.childs = []
        self.isLeaf = False
        self.parent = None
        self.CF = CF(0,np.zeros(d),np.zeros(d))
        self.t = t
        self.b = b
        self.d = d  #dimension

        self.isLeafNode = False
        self.centroid = 0
        self.radius = 0
        self.diameter = 0


    def addLeafNode(self,CFLeafNode):
        self.childs.append(CFLeafNode)
        CFLeafNode.parent = self
        self.update(CFLeafNode)
        if(len(self.childs) == self.b): #need to split
            self.split()

    def popChild(self,idx):
        popped_child = self.childs.pop(idx)
        self.update(self)
        return popped_child

    def getAllDataInCluster(self):
        list = []

        self._getAllDataInCluster(self, list)

        return list

    def _getAllDataInCluster(self, child, list):
        if(child.isLeafNode):
            for x in range (0,len(child.data_ps)):
                list.append(child.data_ps[x].data)
        else :
            if(len(child.childs) > 0):
                for x in range(0,len(child.childs)) :
                    child._getAllDataInCluster(child.childs[x], list)

    def update(self, CFNode):
        self.CF = CF(0,np.zeros(self.d),np.zeros(self.d))
        for x in range(0, len(self.childs)):
            self.CF.add(self.childs[x].CF)

        self.centroid = np.divide(self.CF.ls,self.CF.N)
        data = self.getAllDataInCluster()
        self.radius = [0 for i in range(0,self.d)]

        for x in range(0, len(data)) :
            self.radius = self.radius + (data[x]- self.centroid) * (data[x] - self.centroid)

        self.radius = np.sqrt(np.divide(self.radius,self.CF.N) )

        self.diameter = [0 for i in range(0,self.d)]

        if self.CF.N > 1 :
            for x in range(0, len(data)) :
                for y in range(0, len(data)) :
                    self.diameter = self.diameter + (data[x] - data[y]) * (data[x] - data[y])

            self.diameter = np.sqrt(self.diameter / (self.CF.N * (self.CF.N - 1 ) ))


        if(self.parent != None) :
            self.parent.update(self),

    def split(self):
        index_farthest_points = farthest_points(self.childs)
        index_p1 = min(index_farthest_points[0],index_farthest_points[1])
        index_p2 = max(index_farthest_points[0],index_farthest_points[1])

        #check if we have a parent or if we are the root
        if( self.parent is None ) :
            new_root = CFInnerNode(self.t,self.b,self.d)
            right_side = CFInnerNode(self.t, self.b, self.d)
            idxs_to_pop = []
            for x in range(len(self.childs)):   #decide where which child lands
                if x == index_p1:
                    continue
                if x == index_p2:
                    continue
                if(calculateDistance(self.childs[index_p2],self.childs[x],'euclidian') <=  calculateDistance(self.childs[index_p1],self.childs[x],'euclidian')):
                    #distance to p2 is smaller
                    idxs_to_pop.append(x)

            idxs_to_pop.append(index_p2)  # needed so that during the loop no elemts get removed, which would cause wrong indices
            idxs_to_pop.sort();
            already_popped = 0
            for x in range(len(idxs_to_pop)) :
                right_side.addLeafNode(self.childs[idxs_to_pop[x] - already_popped])
                already_popped = already_popped + 1
            new_root.addLeafNode(self)
            new_root.addLeafNode(right_side)

        else:
            self.parent.addLeafNode(self.popChild(-1))

        return 0

def farthest_points(points):
    x = y = 0
    maxDist= 0
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if i != j:
                dist = calculateDistance(points[i], points[j],'euclidian')
                if dist > maxDist:
                    maxDist = dist
                    x = i
                    y = j
    return [x,y]

class CFLeafNode(object):
    def __init__(self,d,t):
        self.data_ps = []
        self.CF = CF(0,np.zeros(d),np.zeros(d))
        self.isLeafNode = True
        self.parent = None
        self.d = d
        self.t = t

    def addData_p(self,data_p):
        self.data_ps.append(data_p)
        data_p.parent = self
        self.update_CF()

    def removeData_p(self,idx):
        self.data_ps[-1].parent = None
        data_p_deleted = self.data_ps.pop(-1)
        self.update_CF()
        return data_p_deleted

    def update_CF(self):
        self.CF = CF(len(self.data_ps), np.zeros(self.d), np.zeros(self.d))
        for x in range(0, len(self.data_ps)):
            self.CF.ls = self.CF.ls + self.data_ps[x].data;
            self.CF.ss = self.CF.ss + self.data_ps[x].data * self.data_ps[x].data;

        self.centroid = self.CF.ls * (1 / self.CF.N)

        self.radius = [0 for i in range(0, self.d)]

        for x in range(0, len(self.data_ps)):
            self.radius = self.radius + (self.data_ps[x].data - self.centroid) * (self.data_ps[x].data - self.centroid)

        self.radius = np.sqrt(np.divide(self.radius, self.CF.N))

        self.diameter = [0 for i in range(0, self.d)]
        if (self.CF.N > 1):
            for x in range(0, self.CF.N):
                for y in range(0, self.CF.N):
                    self.diameter = self.diameter + (self.data_ps[x].data - self.data_ps[y].data) * (self.data_ps[x].data - self.data_ps[y].data)

            self.diameter = np.sqrt(self.diameter / (self.CF.N * (self.CF.N - 1)))

        for x in range(0, self.d):
            if self.diameter[x] > self.t :  # need create new LeafNode
                new_data_p = self.removeData_p(-1)
                newLeafNode = CFLeafNode(self.d,self.t)
                newLeafNode.addData_p(new_data_p)
                self.parent.addLeafNode(newLeafNode)
                break



        if (self.parent != None):
            self.parent.update(self),

class data_p(object):
    def __init__(self,data):
        self.data = np.array(data)
        self.classLabel = 0
        self.isData = True
        self.parent = None
        self.centroid = np.array(data)  # for comparison

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


def birch(data, t, b):
    # building a CF-tree
    # start with a node which we call root
    root = CFInnerNode(t,b,len(data[0]))

    # creating data points from rows
    data_points = [0 for i in range(len(data))]
    for x in range(0, len(data)):
        data_points[x] = data_p(data[x])


    # add first node by hand
    leaf_node = CFLeafNode(len(data[0]),t)
    leaf_node.addData_p(data_points[0])

    root.addLeafNode(leaf_node);

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
                dist = calculateDistance(newEntry, node.childs[y],'euclidian')
                if dist < minDist:
                    minDist = dist
                    closest = y
            if node.childs[closest].isLeafNode: # we are at a leaf
                distance = minDist
                parent =  node.childs[closest].parent
                break
            node = node.childs[closest]

        # 2. Modifying the leaf   merge then check for threshold condition
        # Would a merge violate the threshold  condition?
        node.childs[closest].addData_p(newEntry)

    test = 0;
    # return list_of_labels
file1 = open('./data/' + 'c_Iris' + '.arff', "rb")
dataset = arff.load(file1)
cl_data = np.array([x[:-1] for x in dataset['data']])

birch(cl_data, 0.03, 5)