import helpers

class Edge(object):
    '''
    represents an object in the stroomgebied
    expects a name, and height of water as flaot
    '''
    def __init__(self,name, height, nodes, stub_param):
        self.name = str(name)
        self.nodes = nodes
        self.height = float(height)
        self.stub_param =  float(stub_param)
    def __str__(self):
        return self.name
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = float(height)
    def decrease_height(self, amount):
        self.height-=float(amount)
    def increase_height(self, amount):
        self.height+=float(amount)
    def get_nodes(self):
        return self.nodes
    def get_stub_param(self):
        return self.stub_param
        
class Node(object):
    def __init__(self, *args):
        self.edges = (args)
    def __str__(self):
        return str([(n.name, n.height, n.stub_param) for n in self.edges])
    def get_edges(self):
        return self.edges
    def get_connected_nodes(self):
        return set(edge.get_nodes for edge in self.edges)
    def displace_water(self):
        '''displaces a Q between all connected nodes so according to the waterheight and neigbouring params'''
        helpers.displacement_stub(self.edges)
        

class Graph(object):
    def __init__(self):
        self.nodes = []
        self.edges = []
    def __str__(self):
        return 'Graph with '+str(len(self.nodes))+' nodes and '+str(len(self.edges))+ ' edges'
    def add_node(self, node):
        self.nodes.append(node)
    def add_edge(self, edge):
        self.edges.append(edge)
    def get_children_of(self, node):
        node.get
    def single_iteration(self, start_node):
        start_node
        


def BFS(graph, start, end, q= []):
    initPath = [start]
    q.append(initPath)
    # q is de list waaraan geappend wordt en representeert de node die straks aan de beurt is het is in de juiste volgorde
    while len(q) != 0:
        # doe iets als de lijst nog vol is
        tmp_path = q.pop(0)
        last_node = tmp_path[len(tmp_path)-1]
        print 'Current path = ', tmp_path
        
         

    return None # als de lijst leeg is.

        
    
        
# test displacement between two edges
e1 = Edge('1',1,0.5)
e2 = Edge('2',2,0.6)
node1 = Node(e1,e2)
print node1
c = 0 
for x in range(100000):
    c+=1
    node1.displace_water()
print node1, '    ', c

