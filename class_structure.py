from helpers import *

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
        print 'Current dequeued path:', tmpPath
        for linkNode in lastNode.get_connected_nodes():
            if linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
                latest_node = newPath[-1]
                if type(latest_node) == Node: 
                    order_of_bfs_iteration.append(latest_node)
    print order_of_bfs_iteration
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
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = float(height)
    def decrease_height(self, amount):
        self.height-=float(amount)
    def increase_height(self, amount):
        self.height+=float(amount)
    def add_node(self,node):
        self.nodes.append(node)
    def get_other_node(self, node):
        for n in self.nodes:
            if n != node:
                return n
    def get_stub_param(self):
        return self.stub_param
#     def get_nodes(self):
#         return self.nodes

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
    def add_water(self, amount):
        self.edges[0].increase_height(amount)
    def remove_water(self):
        self.edges[0].decrease_height(amount)

class Graph(object):
    def __init__(self, name, edges, endnodes, nodes):
        self.name = name
        self.endnodes  = endnodes
        self.nodes = nodes
        self.edges = edges
    def __str__(self):
        return 'Graph with '+str(len(self.nodes))+' nodes and '+str(len(self.edges))+ ' edges'
    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, edge):
        self.edges.append(edge)
    def set_node_sequence(self, start_node):
        self.nodes = get_BFS_iteration_sequence_of_nodes(start_node)
    def single_iteration(self, start_node):
        for n in self.nodes:
            n.displace_water
        


# def BFS_path_creator(graph, start, q= []):
#     current_node = [start]
#     q.append(current_node)
#     # q is de list waaraan geappend wordt en representeert de node die straks aan de beurt is het is in de juiste volgorde
#     while current_node != None:
#         # als er nog een volgende node is, ga dan door
#         q.append(current_node)
#         connected_nodes current_node.get_connected_nodes()
#         
#         tmp_path = q.pop(0)
#           
#            
#   
#     return q # als alle nodes zijn geweest
# 
# def get_BFS_iteration_sequence_of_nodes(start_node):
#     if type(start_node) != EndNode:
#         raise ValueError('First node to iterate from is not of type EndNode')
#     q = []
#     initPath = [start_node]
#     q.append(initPath)
#     order_of_bfs_iteration = []
#     while len(q) != 0:
#         tmpPath = q.pop(0)
#         lastNode = tmpPath[len(tmpPath) - 1]
#         print 'Current dequeued path:', tmpPath
#         for linkNode in lastNode.get_connected_nodes():
#             if linkNode not in tmpPath:
#                 newPath = tmpPath + [linkNode]
#                 q.append(newPath)
#                 latest_node = newPath[1]
#                 if type(latest_node) == Node: 
#                     order_of_bfs_iteration.append(latest_node)
#     return order_of_bfs_iteration
#     
        
# test displacement between four edges and three end points
e1 = Edge(name = '1', height = 1, stub_param = 0.5)
e2 = Edge(name = '2', height = 2, stub_param = 0.6)
e3 = Edge(name = '3', height = 3, stub_param = 0.4)
e4 = Edge(name = '4', height = 3, stub_param = 0.4)
end_node1 = EndNode(e1)
end_node3 = EndNode(e3)
end_node4 = EndNode(e4)
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
