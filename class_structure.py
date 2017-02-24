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
                    endnodes_unknown_flow.append(latest_node)
                if type(latest_node) == Node: 
                    order_of_bfs_iteration.append(latest_node)
    return order_of_bfs_iteration+endnodes_unknown_flow

class Edge(object):
    '''represents an object in the stroomgebied
    '''
    
    
    def __init__(self, name, water_volume, stub_param):
        # params set on init
        self.name = str(name)
        self.water_volume = water_volume 
        self.stub_param =  float(stub_param)
        self.nodes = []
        
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
        
    
    def calculate_set_and_return_slope_and_calculate_discharge(self, water_level_at_end_of_edge):
        water_level_difference_between_middle_and_end = self.water_level-water_level_at_end_of_edge
        self.slope = abs(water_level_difference_between_middle_and_end/(self.length/2)) #divided by two, because self.water_level is the level in the middle of the waterway
        try:
            self.velocity = 1/self.manning_coefficient*self.hydraulic_radius**(2.0/3.0)*self.slope**(1.0/2.0)
        except ValueError:
            raise ValueError('Hydraulic Radius is negative, this is impossible')
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
        self.edges = (args)
    
    def __str__(self):
        return "Node " + str([(e.name, e.water_level, e.stub_param) for e in self.edges])
    
    def get_edges(self):
        return self.edges
    
    def get_connected_nodes(self):
        all_nodes = [edge.get_other_node(self) for edge in self.edges]
        return all_nodes
    
    def displace_water(self):
        '''displaces a Q between all connected nodes according to mannings formula'''
        helpers.displace_water_between_edges(self.edges)


class EndNode(Node):

    
    def __init__(self, edge, discharge):
        self.edges = [edge]
        self.discharge = float(discharge)
        
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
        
   
def test_polder_simple():
    # test displacement between four edges and three end points
    e1 = Edge(name = '1', water_volume= 2, stub_param = 0.05)
    e2 = Edge(name = '2', water_volume= 2, stub_param = 0.05)
    e3 = Edge(name = '3', water_volume= 2, stub_param = 0.05)
    e4 = Edge(name = '4', water_volume= 2, stub_param = 0.05)
    end_node1 = EndNode(edge=e1,discharge=2)
    end_node_UF3 = EndNodeWithUnknownFlow(edge=e3,threshold=4, water_level=0, qh_relationship=helpers.qh_relationship_end_node_unknown_flow_1)
    end_node_UF4 = EndNodeWithUnknownFlow(edge=e4,threshold=4, water_level=0, qh_relationship=helpers.qh_relationship_end_node_unknown_flow_1)
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
    for i in range(10):
        polder.perform_exterior_flow()
#         print [[edge.get_name(),edge.get_water_volume(), edge.get_volume_of_water_passage()] for edge in polder.get_edges()]
        polder.displace_water_between_edges()
        print 'iteration nr: ',i,"    ",[[edge.get_name(),edge.get_water_volume(), edge.get_volume_of_water_passage()] for edge in polder.get_edges()]

# test_polder_simple()
        
        
        
def test_polder_2gemaal_3sloot():
    e1 = Edge(name = '1', water_volume= 600.0, stub_param = 0.05)
    e2 = Edge(name = '2', water_volume= 600.0, stub_param = 0.05)
    e3 = Edge(name = '3', water_volume= 600.0, stub_param = 0.05)
    end_node1 = EndNode(edge=e1,discharge=2.0)
    end_node3 = EndNode(edge=e3,discharge=-2.0)    
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
    polder.set_node_sequence(end_node1)
    for i in range(100):
        polder.perform_exterior_flow()
#         print [[edge.get_name(),edge.get_water_volume(), edge.get_volume_of_water_passage()] for edge in polder.get_edges()]
        polder.displace_water_between_edges()
        print 'iteration nr: ',i,"    ",[[edge.get_name(),'Vol',edge.get_water_volume(), 'Slope', edge.get_slope(), 'Q_real', edge.get_volume_of_water_passage()] for edge in polder.get_edges()]

test_polder_2gemaal_3sloot()
    