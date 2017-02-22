import helpers

def get_BFS_iteration_sequence_of_nodes(start_node):
    if type(start_node) != EndNode:
        raise ValueError('First node to iterate from is not of type EndNode')
    q = []
    initPath = [start_node]
    q.append(initPath)
    order_of_bfs_iteration = []
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
#         print 'Current dequeued path:', tmpPath
        for linkNode in lastNode.get_connected_nodes():
            if linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
                latest_node = newPath[-1]
                if type(latest_node) == Node: 
                    order_of_bfs_iteration.append(latest_node)
#     print order_of_bfs_iteration
    return order_of_bfs_iteration

class Edge(object):
    '''
    represents an object in the stroomgebied
    expects a name, and height of water as flaot
    '''
    def __init__(self, name, height, stub_param):
        self.name = str(name)
        self.height = float(height)
        self.stub_param =  float(stub_param)
        self.nodes = []
    def __str__(self):
        return 'Edge ' +self.name +' ' + str([node.__str__() for node in self.nodes])
    def get_name(self):
        return self.name
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = float(height)
    def adjust_height(self, amount):
        self.height+=float(amount)
    def add_node(self,*args):
        for a in args:
            self.nodes.append(a)
    def get_other_node(self, node):
        for n in self.nodes:
            if n != node:
                return n
    def get_stub_param(self):
        return self.stub_param

class Node(object):
    def __init__(self, *args):
        self.edges = (args)
    def __str__(self):
        return "Node " + str([(e.name, e.height, e.stub_param) for e in self.edges])
    def get_edges(self):
        return self.edges
    def get_connected_nodes(self):
        all_nodes = [edge.get_other_node(self) for edge in self.edges]
        return all_nodes
    def displace_water(self):
        '''displaces a Q between all connected nodes so according to the waterheight and neigbouring params'''
        helpers.displacement_stub(self.edges)

class EndNode(Node):
    def __init__(self, edge, discharge):
        self.edges = [edge]
        self.discharge = float(discharge)
    def adjust_water_height(self):
        self.edges[0].adjust_height(self.discharge)

class Graph(object):
    def __init__(self, name, edges, endnodes, nodes):
        self.name = name
        self.endnodes  = endnodes
        self.nodes = nodes
        self.edges = edges
        self.start_node = None
    def __str__(self):
        return 'Graph with '+str(len(self.nodes))+' nodes and '+str(len(self.edges))+ ' edges'
    def get_edges(self):
        return self.edges
    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, edge):
        self.edges.append(edge)
    def set_node_sequence(self, start_node):
        self.nodes = get_BFS_iteration_sequence_of_nodes(start_node)
    def perform_exterior_flow(self):
        for en in self.endnodes:
            en.adjust_water_height()
    def displace_water_between_nodes(self):
        for n in self.nodes:
            n.displace_water()
        
        
        
def test_polder_loop():
    e1 = Edge(name = '1', height = 500, stub_param = 0.5)
    e2 = Edge(name = '2', height = 500, stub_param = 0.6)
    e3 = Edge(name = '3', height = 500, stub_param = 0.4)
    e4 = Edge(name = '4', height = 500, stub_param = 0.4)
    e5 = Edge(name = '5', height = 500, stub_param = 0.5)
    e6 = Edge(name = '6', height = 500, stub_param = 0.6)
    e7 = Edge(name = '7', height = 500, stub_param = 0.4)
    e8 = Edge(name = '8', height = 500, stub_param = 0.4)
    e9 = Edge(name = '9', height = 500, stub_param = 0.5)
    e10 = Edge(name = '10', height = 500, stub_param = 0.6)
    e11 = Edge(name = '11', height = 500, stub_param = 0.4)
    e12 = Edge(name = '12', height = 500, stub_param = 0.4)
    end_node1 = EndNode(edge=e1,discharge=2)
    end_node6 = EndNode(edge=e6,discharge=-1)
    end_node12 = EndNode(edge=e12,discharge=-1)
    n1d2d7 = Node(e1,e2,e7)
    n2d3 = Node(e2,e3)
    n3d4 = Node(e3,e4)
    n4d5 = Node(e4,e5)
    n5d6d11 = Node(e5,e6,e11)
    n7d8 = Node(e7,e8)
    n8d9d12 = Node(e8,e9,e12)
    n9d10 = Node(e9,e10)
    n10d11 = Node(e10,e11)
    
    e1.add_node(end_node1, n1d2d7)
    e2.add_node(n1d2d7,n2d3)
    e3.add_node(n2d3,n3d4)
    e4.add_node(n3d4,n4d5)
    e5.add_node(n4d5,n5d6d11)            
    e6.add_node(n5d6d11,end_node6)
    e7.add_node(n1d2d7,n7d8)
    e8.add_node(n7d8,n8d9d12)
    e9.add_node(n8d9d12,n9d10)
    e10.add_node(n9d10,n10d11)
    e11.add_node(n10d11,n5d6d11)
    e12.add_node(end_node12,n8d9d12)
    
    edges = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12]
    endnodes = [end_node1, end_node6, end_node12] 
    nodes = [n1d2d7,n2d3,n3d4,n4d5,n5d6d11,n7d8,n8d9d12,n9d10,n10d11] 
    
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    polder.set_node_sequence(end_node1)
    for i in range(30):
        polder.perform_exterior_flow()
        polder.displace_water_between_nodes()
        print [[edge.get_name(),edge.get_height()] for edge in polder.get_edges()]

    
def test_polder_simple():
      
    # test displacement between four edges and three end points
    e1 = Edge(name = '1', height = 500, stub_param = 0.5)
    e2 = Edge(name = '2', height = 500, stub_param = 0.6)
    e3 = Edge(name = '3', height = 500, stub_param = 0.4)
    e4 = Edge(name = '4', height = 500, stub_param = 0.4)
    end_node1 = EndNode(edge=e1,discharge=2)
    end_node3 = EndNode(edge=e3,discharge=-1.3)
    end_node4 = EndNode(edge=e4,discharge=-0.7)
    n12 = Node(e1,e2,e4)
    n23 = Node(e2,e3)
    e1.add_node(end_node1)
    e1.add_node(n12)
    e2.add_node(n12)
    e2.add_node(n23)
    e3.add_node(n23)
    e3.add_node(end_node3)
    e4.add_node(n12)
    e4.add_node(end_node4) 
        
    edges = [e1,e2,e3,e4]
    endnodes = [end_node1, end_node3, end_node4]
    nodes = [n12,n23]
    
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    polder.set_node_sequence(end_node1)
    for i in range(80):
        polder.perform_exterior_flow()
        polder.displace_water_between_nodes()
    print [[edge.get_name(),edge.get_height()] for edge in polder.get_edges()]

test_polder_simple()
        
        