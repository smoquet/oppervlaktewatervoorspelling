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
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
#         print 'Current dequeued path:', tmpPath
        for linkNode in lastNode.get_connected_nodes():
            if linkNode != None and linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
                latest_node = newPath[-1]
                if type(latest_node) == Node or type(latest_node) == Weir: 
                    if latest_node not in order_of_bfs_iteration:
                        order_of_bfs_iteration.append(latest_node)
    return order_of_bfs_iteration

class Edge(object):
    '''represents a ditch
    '''
    
    
    def __init__(self, name, water_volume, manning_coefficient = 0.013, bottom_level=1.0, salinity=0.005):
        # params set on init
        self.name = str(name)
        self.water_volume = water_volume 
        self.salinity = salinity
        self.nodes = []
        self.water_direction = None
        self.take_salinity_into_account = False
        
        # params to be set on init eventually
        self.manning_coefficient = manning_coefficient
        self.length = 100.0 
        self.talus = 0.0 # 0.5 = talud 1 meter omlaag is 0.5 meter opzij
        self.bottom_width = 5.0 #bodem breedte
        self.bottom_level = bottom_level #bodem niveau
        
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
    
    def _get_volume_of_water_passage(self):
        return self.volume_of_water_passage
    
    def _adjust_parameters_after_water_displacement(self):
        self.water_depth = self.water_depth_to_volume_ratio*self.water_volume
        self.water_level = self.water_depth+self.bottom_level
        self.water_depth+self.bottom_level
        self.water_surface_width = self.bottom_width+2.0*(self.water_depth*self.talus)
        self.wetted_perimeter = self.bottom_width + 2.0*(((self.water_surface_width-self.bottom_width)/2.0)**2.0 + self.water_depth**2.0)**0.5
        self.cross_sectional_area_of_flow = self.water_depth*(self.bottom_width+self.water_surface_width)/2.0
        self.hydraulic_radius = self.cross_sectional_area_of_flow/self.wetted_perimeter
    
    def get_name(self):
        return self.name
    
    def get_water_level(self):
        return self.water_level
    
    def get_slope(self):
        return self.slope
    
    def update_water_direction(self, node):
        self.water_direction = node
    
    def get_water_direction(self):
        return self.water_direction
    
    def set_water_direction(self, node):
        self.water_direction = node
    
#     def set_take_salinity_into_account(self, bool):
#         self.take_salinity_into_account = bool
    
    def calculate_surplus_Q(self, max_height):
        '''returns the surplus of Q, given that it's height may not exceed the max_height
        '''
        water_height_difference = self.water_level - max_height
        if water_height_difference <= 0: # no surplus 
            return 0.0
        else:  
            surplus_Q = water_height_difference/self.water_depth_to_volume_ratio
            return surplus_Q
    
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
    
#     def reset_params_before_water_displacement(self):
# #         self.volume_of_water_passage = 0.0
#         self.water_direction = None
        
    def adjust_water_volume(self, volume):
        self.water_volume += volume
        self._adjust_parameters_after_water_displacement()
        if volume <= 0:
            self.volume_of_water_passage=volume
#             print [[edge.name, edge.volume_of_water_passage] for edge in self.nodes[0].graph.get_edges()]
    
#     def adjust_water_volume_and_salinity(self, volume, salinity_of_volume):
#         current_salt = self.water_volume*self.salinity
#         salt_to_add = volume * salinity_of_volume
#         salt_total = current_salt+salt_to_add 
#         self.water_volume += volume
#         self.salinity = salt_total/self.water_volume

    
    def add_node(self,*args):
        for a in args:
            self.nodes.append(a)
    
    def get_other_node(self, node):
        for n in self.nodes:
            if n != node:
                return n
    def get_nodes(self):
        return self.nodes


class EndEdge(Edge):
    def adjust_water_volume(self, volume):
        pass
    

class Node(object):
    '''represents a connection between edges
    it has at least two edges, no maximum number of edges
    '''
  
    def __init__(self, *args):
        self.edges = args
        self.name = 'Node '
        self.graph =None
        for e in self.edges:
            self.name += '-'+(e.name)
        
    def __str__(self):
        return self.name
    
    def get_edges(self):
        return self.edges
    
    def get_connected_nodes(self):
        all_nodes = [edge.get_other_node(self) for edge in self.edges]
        return all_nodes
    
    def set_take_salinity_into_account(self, bool):
        self.take_salinity_into_account = bool
    
    def displace_water(self):
        '''displaces a Q between all connected nodes according to mannings formula'''
#         for edge in self.edges:
#             edge.reset_params_before_water_displacement()
        helpers.displace_water_between_edges(self)

    def add_graph(self, graph):
        self.graph = graph

class EndNode(Node):
    '''(this is a pump or 'gemaal') this type of node has a fixed in or output
    it must have one edge
    '''
    
    def __init__(self, edge, discharge, salinity=0.0):
        self.edges = [edge]
        self.salinity = salinity
        self.discharge = float(discharge)
        self.name = 'Endnode'+self.edges[0].name
#         self.take_salinity_into_account = False
        
    def add_or_reduce_water(self):
        
        self.edges[0].adjust_water_volume(self.discharge)
        if self.discharge <0.0:
            self.edges[0].set_water_direction(self)
    

class Weir(Node):
    '''this type of node represents a weir or 'stuw'
     it must have two edges
    '''
    
    def __init__(self, edges, weir_constant, width, height):
        if len(edges) > 2:
            raise ValueError('Weir does not have two edges associated with it, it has %d' % len(edges))
        self.edges = edges
        self.weir_constant = weir_constant
        self.width = width
        self.height = height
        self.take_salinity_into_account = False
        self.name = 'Weir '
        for e in self.edges:
            self.name += '-'+(e.name)

    def get_other_edge(self, edge):
        for e in self.edges:
            if e != edge:
                return e
        
    def one_edge_has_higher_water_level_other_lower_than_weir_height(self):
        edge1_water_level = self.edges[0].get_water_level()
        edge2_water_level = self.edges[1].get_water_level()
        if edge1_water_level > self.height and edge2_water_level < self.height:
            return True 
        elif edge1_water_level < self.height and edge2_water_level > self.height:
            return True
        return False
        
    def both_edges_have_lower_water_levels_or_both_have_same_level_as_weir_height(self):
        edge1_water_level = self.edges[0].get_water_level()
        edge2_water_level = self.edges[1].get_water_level()
        if edge1_water_level < self.height and edge2_water_level < self.height:
            return True
        elif edge1_water_level == self.height and edge2_water_level == self.height:
            return True
        return False
        
    def displace_water(self):
        for edge in self.edges:
            edge.reset_params_before_water_displacement()
        if self.one_edge_has_higher_water_level_other_lower_than_weir_height():
            helpers.weir_displace_water_between_edges(self) # in this case the weir has effect and its own method is used
        elif self.both_edges_have_lower_water_levels_or_both_have_same_level_as_weir_height():
            pass # in this case nothing happens
        else: # both_edges_have_higher_water_levels_or_one_has_same_level_and_other_is_higher
            super(Weir, self).displace_water() # in this case the parent's method is used
                
           

class Graph(object):
    ''' represents the whole system (all the nodes and edges)
    '''
    
    def __init__(self, name, edges, endnodes, nodes, start_node=None):
        self.name = name
        self.endnodes  = endnodes
        self.nodes = nodes
        self.edges = edges
        self.start_node = start_node
        self.add_nodes_to_edges()
    
    def __str__(self):
        try:
            printable_string = 'Graph with edges' +str([[edge.name, 
                                                 edge.water_volume, 
                                                 edge.volume_of_water_passage,  
                                                 edge.salinity, 
                                                 edge.water_direction.name
                                                 ] for edge in self.edges])
        except:
            printable_string = 'Graph with edges' +str([[edge.name, 
                                                 edge.water_volume, 
                                                 edge.volume_of_water_passage,  
                                                 edge.salinity, 
                                                 'no direction'
                                                 ] for edge in self.edges])
        return printable_string
    
    def add_nodes_to_edges(self):
        for node in self.nodes+self.endnodes:
            for edge in node.get_edges():
                edge.add_node(node)
    
    def get_edges(self):
        return self.edges
    
    def get_discharge_volume_and_salinity_values(self):
        result = {}
        for edge in self.edges:
            result[edge] = (edge.water_volume,edge.salinity)
        return result
    
    def get_node_sequence(self):
        return [node.name for node in self.nodes]
    
    def get_total_volume_of_water_passage(self):
        total_volume_of_water_passage = 0.0
        for edge in self.edges:
            total_volume_of_water_passage+=edge.volume_of_water_passage
        return total_volume_of_water_passage
    
    def add_node(self, node):
        self.nodes.append(node)
    
    def add_edge(self, edge):
        self.edges.append(edge)
    
    def set_node_sequence(self, start_node):
        self.nodes = get_BFS_iteration_sequence_of_nodes(start_node)
    
    def perform_exterior_flow(self):
        '''all the endnodes produce their discharge
        '''
        for en in self.endnodes:
            en.add_or_reduce_water()
    
    def displace_water_between_edges(self):
        '''all the internal nodes or weirs displace water between their edges
        '''
        for n in self.nodes:
            n.displace_water()

    def get_total_water_in_system(self):
        total_water = 0.0
        for edge in self.get_edges():
            total_water+=edge.get_water_volume()
        return total_water

    def reach_flow_balance(self, max_iterations=1000, debug=False):
        ''' loop through external flow and internal displacement between edges
        for a set number of iterations
        TODO: implement a criteria for balance
        '''
        self.set_node_sequence(self.start_node)
        previous_total_volume_of_water_passage = 0.0
        for i in range(max_iterations):
            if i < 20:
                self.perform_exterior_flow()
                self.displace_water_between_edges()
                if debug:
                    print 'Iteration nr: ',i,' ', self
            else:
                if i == 800:
                    pass #place breakpoint here
                
#                 BALANCE CRITERIUM:
                if abs(self.get_total_volume_of_water_passage()-previous_total_volume_of_water_passage) >= 0.000000001 and i < max_iterations:

#                 if i < max_iterations:
                    previous_total_volume_of_water_passage = self.get_total_volume_of_water_passage()
                    self.perform_exterior_flow()
                    self.displace_water_between_edges()
                    if debug:
                        print 'Iteration nr: ',i,' ', self

    # TODO: implement salinity displacement:
#     def displace_salinity(self, timesteps = 500, debug=False):
#         for i in range(timesteps):
#             for endnode in self.endnodes:
#                 endnode.displace_water_and_salinity_according_to_balance()
#             for node in self.nodes:
#                 node.displace_water_and_salinity_according_to_balance()
                
'''    
# TESTS

1) creeer alle edges (sloten)
2) creeer alle endnodes (gemalen) en wijs deze de edges toe waar ze aan verbonden zijn
3) creer alle nodes en wijs deze de edges toe die er aan verbonden zijn
4) voeg voor elke edge de nodes toe die er aan vast zitten
5) creeer een graph met deze nodes, endnodes en edges
5b) itereer om een belans te verkrijgen (graph.reach_flow_balance)
        - debug=True voor print statements
        - voor en na reach_flow_balance kun je de hoeveelheid water bijhouden om lekkages te detecteren


'''

# def add_nodes_to_edges(nodes):
#     for node in nodes:
#         for edge in node.get_edges():
#             edge.add_node(node)
            

    
def test_polder_flow_balance_test_2gemaal_3sloot():
#     1
    e1 = Edge(name = '1', water_volume= 750.0)
    e2 = Edge(name = '2', water_volume= 750.0)
    e3 = Edge(name = '3', water_volume= 750.0)
#     2
    end_node1 = EndNode(edge=e1,discharge=0.025)
    end_node3 = EndNode(edge=e3,discharge=-0.025)
#     3
    n12 = Node(e1,e2)
    n23 = Node(e2,e3)
#     4
    e1.add_node(end_node1)
    e1.add_node(n12)
    e2.add_node(n12)
    e2.add_node(n23)
    e3.add_node(n23)
    e3.add_node(end_node3)
#     5
    edges = [e1,e2,e3]
    endnodes = [end_node1,end_node3] 
    nodes = [n12,n23]
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
#     5b
    a = polder.get_total_water_in_system()
    polder.reach_flow_balance(debug=True)
    print a-polder.get_total_water_in_system()
    print polder
    
# test_polder_flow_balance_test_2gemaal_3sloot()

def test_polder_2gemaal_3sloot():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0)
    end_node1 = EndNode(edge=e1,discharge=20)
    end_node3 = EndNode(edge=e3,discharge=-20)    
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
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations= 100, debug=True)
    print polder
    
# test_polder_2gemaal_3sloot()

def test_polder_5gemaal_10sloot():
    e1 = Edge(name = '1', water_volume= 6000.0)
    e2 = Edge(name = '2', water_volume= 6000.0)
    e3 = Edge(name = '3', water_volume= 6000.0)
    e4 = Edge(name = '4', water_volume= 6000.0)
    e5 = Edge(name = '5', water_volume= 6000.0)
    e6 = Edge(name = '6', water_volume= 6000.0)
    e7 = Edge(name = '7', water_volume= 6000.0)
    e8 = Edge(name = '8', water_volume= 6000.0)
    e9 = Edge(name = '9', water_volume= 6000.0)
    e10 = Edge(name = '10', water_volume= 6000.0)
    e11 = Edge(name = '11', water_volume= 6000.0)
    end_node1 = EndNode(edge=e1,discharge=-25)
    end_node2 = EndNode(edge=e2,discharge=-25)    
    end_node6 = EndNode(edge=e6,discharge=25)
    end_node7 = EndNode(edge=e7,discharge=-25)    
    end_node11 = EndNode(edge=e11,discharge=50)
    n1d2d3 =    Node(e1,e2,e3)
    n3d4d5d6 =  Node(e3,e4,e5,e6)
    n4d7d8 =    Node(e4,e7,e8)
    n5d9 =      Node(e5,e9)
    n8d10 =     Node(e8,e10)
    n9d10d11 =  Node(e9,e10,e11)
    
    edges = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11]
    endnodes = [end_node1,end_node2,end_node6,end_node7,end_node11]
    nodes = [n1d2d3,n3d4d5d6,n4d7d8,n5d9,n8d10,n9d10d11]
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    a = polder.get_total_water_in_system()
    polder.reach_flow_balance(max_iterations= 80, debug=True)
    print a - polder.get_total_water_in_system()
    

# test_polder_5gemaal_10sloot()

def test_polder_cirkel():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0, manning_coefficient=0.75)
    e4 = Edge(name = '4', water_volume= 600.0)
    e5 = Edge(name = '5', water_volume= 600.0)
    end_node1 = EndNode(edge=e1,discharge=-0.02)
    end_node5 = EndNode(edge=e5,discharge=0.02)    
    n1d2d3 =    Node(e1,e2,e3)
    n2d4 =  Node(e2,e4)
    n3d4d5 =    Node(e3,e4,e5)
    
    edges = [e1,e2,e3,e4,e5]
    endnodes = [end_node1,end_node5]
    nodes = [n1d2d3,n2d4,n3d4d5]
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node5)
    polder.reach_flow_balance(max_iterations=1000, debug=True)
    print polder
    
# test_polder_cirkel()

def test_polder_2gemaal_4sloot():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0, manning_coefficient=0.075)
    e4 = Edge(name = '4', water_volume= 600.0)
    
    end_node1 = EndNode(edge=e1,discharge=-0.2)
    end_node4 = EndNode(edge=e4,discharge=0.2)    
    n1d2d3 =    Node(e1,e2,e3)
    n2d3d4 =  Node(e2,e3,e4)
    
    edges = [e1,e2,e3,e4]
    endnodes = [end_node1,end_node4]
    nodes = [n1d2d3,n2d3d4]
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    totaal = polder.get_total_water_in_system()
    polder.reach_flow_balance(debug=True)
    print totaal - polder.get_total_water_in_system()
    
test_polder_2gemaal_4sloot()

def test_polder_1gemaal_2sloot_water_drempel_check():
    e1 = Edge(name = '1', water_volume= 800.0 )
    e2 = Edge(name = '2', water_volume= 1000.0, bottom_level=5.0)
    
    end_node1 = EndNode(edge=e1,discharge=50)
    end_node2 = EndNode(edge=e2,discharge=0)
    n1d2 =    Node(e1,e2)
    edges = [e1,e2]
    endnodes = [end_node1, end_node2]
    nodes = [n1d2]
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=50, debug=True)
    print polder
    
# test_polder_1gemaal_2sloot_water_drempel_check()

def test_EndEdge_sloot():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    end_edge3 = EndEdge(name = 'end3', water_volume=500.0)
    
    end_node1 = EndNode(edge=e1,discharge=0.02)
    
    n1d2 =    Node(e1,e2)
    n2end3 =    Node(e2,end_edge3)
    
    edges = [e1,e2, end_edge3]
    endnodes = [end_node1]
    nodes = [n1d2, n2end3]    
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=500, debug=True)
    print polder

# test_EndEdge_sloot()

def test_weir_simple():
    e1 = Edge(name = '1', water_volume= 1000.0)
    e2 = Edge(name = '2', water_volume= 1000.0)
    e3 = Edge(name = '3', water_volume= 1000.0)
        
    end_node1 = EndNode(edge=e1,discharge=60)
    end_node3 = EndNode(edge=e3,discharge=-60)
    
    n1d2 = Weir(edges= [e1,e2], weir_constant=1.6, width=6, height=2.3)
    n2d3 = Node(e2,e3)
    
    edges = [e1,e2,e3]
    endnodes = [end_node1, end_node3]
    nodes = [n1d2, n2d3]    
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=150, debug=True)
    print polder

# test_weir_simple()

def test_moat_fill():
    e1 = Edge(name = '1', water_volume= 3625.0)
    e2 = Edge(name = '2', water_volume= 4357.0)
    e3 = Edge(name = '3', water_volume= 3897.0)
        
    end_node1 = EndNode(edge=e1,discharge=0.3)
    end_node3 = EndNode(edge=e3,discharge=-0.3)
    
    n1d2 = Node(e1,e2)
    n2d3 = Node(e2,e3)
    
    edges = [e1,e2,e3]
    endnodes = [end_node1, end_node3]
    nodes = [n1d2, n2d3]
#       add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=1000, debug=True)
    print polder
    

# test_moat_fill()

def test_two_moat_balance():

    e1 = Edge(name = '1', water_volume= 3625.0, manning_coefficient=0.075)
    e2 = Edge(name = '2', water_volume= 4357.0)
        
    end_node1 = EndNode(edge=e1,discharge=0)
    
    n1d2 = Node(e1,e2)
    
    edges = [e1,e2]
    endnodes = [end_node1]
    nodes = [n1d2]
#     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=500, debug=True)
    print polder
    
# test_two_moat_balance()

def test_weir():
    e1 = Edge(name = '1', water_volume= 600.0)
    e2 = Edge(name = '2', water_volume= 600.0)
    e3 = Edge(name = '3', water_volume= 600.0)
    e4 = EndEdge(name = '4', water_volume= 599.0)
    e5 = Edge(name = '5', water_volume= 600.0)
    e6 = Edge(name = '6', water_volume= 600.0)
    e7 = EndEdge(name = '7', water_volume= 599.0)
        
    end_node1 = EndNode(edge=e1,discharge=20)
    
    n1d2d5 = Node(e1,e2,e5)
    n2d3 = Weir(edges= [e2,e3], weir_constant=1.6, width=6, height=2.3)
    n3d4 = Node(e3,e4)
    n5d6 = Node(e5,e6)
    n6d7 = Node(e6,e7)
    
    edges = [e1,e2, e3,e4,e5,e6,e7]
    endnodes = [end_node1]
    nodes = [n1d2d5,n2d3,n3d4,n5d6,n6d7]
    #     add_nodes_to_edges(nodes+endnodes)
    polder = Graph(name = 'polder', edges = edges, endnodes = endnodes, nodes = nodes, start_node=end_node1)
    polder.reach_flow_balance(max_iterations=45, debug=True)
    print polder

# test_weir()
