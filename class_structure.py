import helpers

def get_BFS_iteration_sequence_of_nodes(start_node):
    if type(start_node) != EndNode:
        raise ValueError('First node to iterate from is not of type EndNode')
    q = []
    initPath = [start_node]
    q.append(initPath)
    order_of_bfs_iteration = []
    endnodes_unknown_flow = []
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
#         print 'Current dequeued path:', tmpPath
        for linkNode in lastNode.get_connected_nodes():
            if linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
                latest_node = newPath[-1]
                if type(latest_node) == EndNodeWithUnknownFlow:
                    endnodes_unknown_flow.append(latest_node)
                if type(latest_node) == Node: 
                    order_of_bfs_iteration.append(latest_node)
    return order_of_bfs_iteration+endnodes_unknown_flow

class Edge(object):
    '''
    represents an object in the stroomgebied
    expects a name, and height of water as flaot
    '''
    def __init__(self, name, water_volume, stub_param):
        self.name = str(name)
        self.water_volume = water_volume 
        self.stub_param =  float(stub_param)
        self.nodes = []
        self.height_volume_ratio = 1
        self.height = self.height_volume_ratio*self.water_volume
        self.water_volume_passage = 0
    def __str__(self):
        return 'Edge ' +self.name +' ' + str([node.__str__() for node in self.nodes])
    def get_name(self):
        return self.name
    def get_height(self):
        return self.height
    def adjust_height_to_water_volume(self):
        self.height = self.height_volume_ratio*self.water_volume
    def get_water_volume(self):
        return self.water_volume
    def get_height_volume_ratio(self):
        return self.height_volume_ratio
    def adjust_water_volume(self, volume):
        self.water_volume += volume
        self.adjust_height_to_water_volume()
        if volume <0:
            self.water_volume_passage=volume
    def add_node(self,*args):
        for a in args:
            self.nodes.append(a)
    def get_other_node(self, node):
        for n in self.nodes:
            if n != node:
                return n
    def get_stub_param(self):
        return self.stub_param
    def get_water_volume_passage(self):
        return self.water_volume_passage


#     def adjust_height(self, amount):
#         self.height+=float(amount)


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
    def add_or_reduce_water(self):
        self.edges[0].adjust_water_volume(self.discharge)

class EndNodeWithUnknownFlow(Node):
    def __init__(self, edge, threshold):
        self.edges = [edge]
        self.threshold = threshold
    def get_threshold(self):
        return self.threshold
    def displace_water(self):
        helpers.edge_flow_stub(self)
    
        
        
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
            en.add_or_reduce_water()
    def displace_water_between_nodes(self):
        for n in self.nodes:
            n.displace_water()
        
   
def test_polder_simple():
      
    # test displacement between four edges and three end points
    e1 = Edge(name = '1', water_volume= 500, stub_param = 1)
    e2 = Edge(name = '2', water_volume= 500, stub_param = 1)
    e3 = Edge(name = '3', water_volume= 500, stub_param = 1)
    e4 = Edge(name = '4', water_volume= 500, stub_param = 1)
    end_node1 = EndNode(edge=e1,discharge=2)
    end_node_UF3 = EndNodeWithUnknownFlow(edge=e3,threshold=500)
    end_node_UF4 = EndNodeWithUnknownFlow(edge=e4,threshold=500)
    n12 = Node(e1,e2,e4)
    n23 = Node(e2,e3)
    e1.add_node(end_node1)
    e1.add_node(n12)
    e2.add_node(n12)
    e2.add_node(n23)
    e3.add_node(n23)
    e3.add_node(end_node_UF3)
    e4.add_node(n12)
    e4.add_node(end_node_UF4) 
        
    edges = [e1,e2,e3,e4]
    endnodes = [end_node1] 
    nodes = [n12,n23, end_node_UF3, end_node_UF4]
    
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    polder.set_node_sequence(end_node1)
    for i in range(800):
        polder.perform_exterior_flow()
#         print [[edge.get_name(),edge.get_water_volume(), edge.get_water_volume_passage()] for edge in polder.get_edges()]
        polder.displace_water_between_nodes()
        print [[edge.get_name(),edge.get_water_volume(), edge.get_water_volume_passage()] for edge in polder.get_edges()]

test_polder_simple()
        
        