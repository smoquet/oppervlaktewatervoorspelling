import helpers
   
    
def get_BFS_iteration_sequence_of_nodes(start_node):
    '''returns a list of nodes in a breadth first search order
    '''
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
                    if latest_node not in endnodes_unknown_flow: 
                        endnodes_unknown_flow.append(latest_node)
                if type(latest_node) == Node: 
                    if latest_node not in order_of_bfs_iteration:
                        order_of_bfs_iteration.append(latest_node)
    return order_of_bfs_iteration+endnodes_unknown_flow

class Edge(object):
    '''represents an object in the stroomgebied
    '''
    
    
    def __init__(self, name, water_volume):
        # params set on init
        self.name = str(name)
        self.water_volume = water_volume 
        self.nodes = []
        self.water_direction = None
        
        # params to be set on init eventually
        self.manning_coefficient = 0.013
        self.length = 100.0 
        self.talus = 0.0 #talud 1 meter omlaag is 0.5 meter opzij
        self.bottom_width = 5.0 #bodem breedte
        self.bottom_level = 1.0 #bodem niveau
        
        # params to calculate on initialisation
        self.water_depth_to_volume_ratio = 1/(self.bottom_width*self.length)

        # params to calculate after water displacement
        self.water_depth = self.water_depth_to_volume_ratio*self.water_volume
        self.water_level = self.water_depth+self.bottom_level
        self.water_surface_width = self.bottom_width+2.0*(self.water_depth*self.talus)
        self.wetted_perimeter = self.bottom_width + 2.0*(((self.water_surface_width-self.bottom_width)/2.0)**2.0 + self.water_depth**2.0)**0.5
        self.cross_sectional_area_of_flow = self.water_depth*(self.bottom_width+self.water_surface_width)/2.0
        self.hydraulic_radius = self.cross_sectional_area_of_flow/self.wetted_perimeter
        # this one is calculated seperatly after water displacement
        self.volume_of_water_passage = 0.0
        
        # params to calculate before water displacement
        self.slope = 0.0
        self.velocity = 1/self.manning_coefficient*self.hydraulic_radius**(2.0/3.0)*self.slope**(1.0/2.0)
        self.discharge = self.velocity*self.cross_sectional_area_of_flow
        
    def __str__(self):
        return 'Edge ' +self.name +' level: ' +str(self.water_level)+ ' volume: '+str(self.water_volume)+' Q: '+str(self.volume_of_water_passage) 
    
    def get_name(self):
        return self.name
    
    def get_water_level(self):
        return self.water_level
    
    def get_slope(self):
        return self.slope
    
    def adjust_parameters_after_water_displacement(self):
        self.water_depth = self.water_depth_to_volume_ratio*self.water_volume
        self.water_level = self.water_depth+self.bottom_level
        self.water_depth+self.bottom_level
        self.water_surface_width = self.bottom_width+2.0*(self.water_depth*self.talus)
        self.wetted_perimeter = self.bottom_width + 2.0*(((self.water_surface_width-self.bottom_width)/2.0)**2.0 + self.water_depth**2.0)**0.5
        self.cross_sectional_area_of_flow = self.water_depth*(self.bottom_width+self.water_surface_width)/2.0
        self.hydraulic_radius = self.cross_sectional_area_of_flow/self.wetted_perimeter
    
    def update_water_direction(self, node):
        self.water_direction = node
    
    def get_water_direction(self):
        return self.water_direction
    
    def calculate_set_and_return_slope_and_calculate_discharge(self, water_level_at_end_of_edge):
        water_level_difference_between_middle_and_end = self.water_level-water_level_at_end_of_edge
        self.slope = abs(water_level_difference_between_middle_and_end/(self.length/2)) #divided by two, because self.water_level is the level in the middle of the waterway
        try:
            self.velocity = 1/self.manning_coefficient*self.hydraulic_radius**(2.0/3.0)*self.slope**(1.0/2.0)
        except ValueError:
            raise ValueError('Hydraulic Radius is negative, system has dried out somewhere')
        self.discharge = self.velocity*self.cross_sectional_area_of_flow
        return self.slope
    
    def get_water_volume(self):
        return self.water_volume
    
    def get_height_volume_ratio(self):
        return self.height_volume_ratio
    
    def get_water_depth_to_volume_ratio(self):
        return self.water_depth_to_volume_ratio
    
    def get_discharge_Q(self):
        return self.discharge
    
    def adjust_water_volume(self, volume):
        self.water_volume += volume
        self.adjust_parameters_after_water_displacement()
        if volume <0:
            self.volume_of_water_passage=volume
    
    def add_node(self,*args):
        for a in args:
            self.nodes.append(a)
    
    def get_other_node(self, node):
        for n in self.nodes:
            if n != node:
                return n
    
    def get_stub_param(self):
        return self.stub_param
    
    def get_volume_of_water_passage(self):
        return self.volume_of_water_passage



class Node(object):

    
    def __init__(self, *args):
        self.edges = args
        self.name = 'Node '
        for e in self.edges:
            self.name += '-'+(e.name)
        
    def __str__(self):
        return self.name
    
    def get_edges(self):
        return self.edges
    
    def get_connected_nodes(self):
        all_nodes = [edge.get_other_node(self) for edge in self.edges]
        return all_nodes
    
    def displace_water(self):
        '''displaces a Q between all connected nodes according to mannings formula'''
        helpers.displace_water_between_edges(self)


class EndNode(Node):

    
    def __init__(self, edge, discharge):
        self.edges = [edge]
        self.discharge = float(discharge)
        self.name = 'Endnode'+self.edges[0].name
        
    def add_or_reduce_water(self):
        self.edges[0].adjust_water_volume(self.discharge)


class EndNodeWithUnknownFlow(Node):
    
    
    def __init__(self, edge, threshold, water_level, qh_relationship):
        self.edges = [edge]
        self.threshold = threshold # absolute value, not relative to bottom of waterway
        self.water_level = water_level
        self.qh_relationship = qh_relationship
        
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
    
    def get_node_sequence(self):
        return [node.name for node in self.nodes]
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def set_node_sequence(self, start_node):
        self.nodes = get_BFS_iteration_sequence_of_nodes(start_node)
    
    def perform_exterior_flow(self):
        for en in self.endnodes:
            en.add_or_reduce_water()
    
    def displace_water_between_edges(self):
        for n in self.nodes:
            n.displace_water()

# TESTS

        
def add_nodes_to_edges(nodes):
    for node in nodes:
        for edge in node.get_edges():
            edge.add_node(node)
def total_water_in_system(polder):
    total_water = 0
    for edge in polder.get_edges():
        total_water+=edge.get_water_volume()
    return total_water

def run_polder(polder, start_node, iterations, print_each_iter=False):
    polder.set_node_sequence(start_node)
    print polder.get_node_sequence()
    total_water_at_start = total_water_in_system(polder)
    
    for i in range(iterations):
        total_water_displacement = 0
        print '\n'
        polder.perform_exterior_flow()
    #         print [[edge.get_name(),edge.get_water_volume(), edge.get_volume_of_water_passage()] for edge in polder.get_edges()]
        polder.displace_water_between_edges()
        if print_each_iter:
            for edge in polder.get_edges():
                total_water_displacement+=edge.get_volume_of_water_passage()
                print 'iteration nr:',i,[edge.get_name(),'Vol',edge.get_water_volume(), 'Slope', edge.get_slope(), 'Q-calc', edge.get_discharge_Q(),'Q_real', edge.get_volume_of_water_passage(), 'dir:',str(edge.get_water_direction())]
            print total_water_displacement/len(polder.get_edges())

    for edge in polder.get_edges():
        print 'iteration nr:',i,[edge.get_name(),'Vol',edge.get_water_volume(), 'Slope', edge.get_slope(), 'Q-calc', edge.get_discharge_Q(),'Q_real', edge.get_volume_of_water_passage(), 'dir:',str(edge.get_water_direction())]
    print 'water_difference = ' ,total_water_at_start-total_water_in_system(polder)
        
def test_polder_2gemaal_3sloot():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 400.0)
    e3 = Edge(name = '3', water_volume= 600.0)
    end_node1 = EndNode(edge=e1,discharge=0)
    end_node3 = EndNode(edge=e3,discharge=0)    
    n12 = Node(e1,e2)
    n23 = Node(e2,e3)
    e1.add_node(end_node1)
    e1.add_node(n12)
    e2.add_node(n12)
    e2.add_node(n23)
    e3.add_node(n23)
    e3.add_node(end_node3)
    
    edges = [e1,e2,e3]
    endnodes = [end_node1,end_node3] 
    nodes = [n12,n23]
    
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    run_polder(polder, end_node1, 10, print_each_iter=True)
    
# test_polder_2gemaal_3sloot()

def test_polder_5gemaal_10sloot():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0)
    e4 = Edge(name = '4', water_volume= 600.0)
    e5 = Edge(name = '5', water_volume= 600.0)
    e6 = Edge(name = '6', water_volume= 600.0)
    e7 = Edge(name = '7', water_volume= 600.0)
    e8 = Edge(name = '8', water_volume= 600.0)
    e9 = Edge(name = '9', water_volume= 600.0)
    e10 = Edge(name = '10', water_volume= 600.0)
    e11 = Edge(name = '11', water_volume= 600.0)
    end_node1 = EndNode(edge=e1,discharge=-30.0)
    end_node2 = EndNode(edge=e2,discharge=-30.0)    
    end_node6 = EndNode(edge=e6,discharge=20.0)
    end_node7 = EndNode(edge=e7,discharge=20.0)    
    end_node11 = EndNode(edge=e11,discharge=20.0)
    n1d2d3 =    Node(e1,e2,e3)
    n3d4d5d6 =  Node(e3,e4,e5,e6)
    n4d7d8 =    Node(e4,e7,e8)
    n5d9 =      Node(e5,e9)
    n8d10 =     Node(e8,e10)
    n9d10d11 =  Node(e9,e10,e11)
    
    edges = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11]
    endnodes = [end_node1,end_node2,end_node6,end_node7,end_node11]
    nodes = [n1d2d3,n3d4d5d6,n4d7d8,n5d9,n8d10,n9d10d11]
    add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    run_polder(polder, end_node1, 150, print_each_iter=True)

test_polder_5gemaal_10sloot()

def test_polder_cirkel():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0)
    e4 = Edge(name = '4', water_volume= 600.0)
    e5 = Edge(name = '5', water_volume= 600.0)
    end_node1 = EndNode(edge=e1,discharge=-20)
    end_node5 = EndNode(edge=e5,discharge=20)    
    n1d2d3 =    Node(e1,e2,e3)
    n2d4 =  Node(e2,e4)
    n3d4d5 =    Node(e3,e4,e5)
    
    edges = [e1,e2,e3,e4,e5]
    endnodes = [end_node1,end_node5]
    nodes = [n1d2d3,n2d4,n3d4d5]
    add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes)
    run_polder(polder, end_node5, 50, print_each_iter=True)

    
# test_polder_cirkel()