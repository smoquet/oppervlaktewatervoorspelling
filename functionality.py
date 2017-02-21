import class_structure as c

a = c.Node('a',2)
b = c.Node('a',0)
c = c.Node('a',0)
d = c.Node('a',0)
e = c.Node('a',0)
f = c.Node('a',0)

ab = e.Edge(a,b)
ac = e.Edge(a,c)
bd = e.Edge(b,d)
be = e.Edge(b,e)
ef = e.Edge(e,f)
cf = e.Edge(c,f)


def breadth_first_equation_iteration(startnode, q=[]):
    init_equated_nodes = [startnode]
    q.append(init_equated_nodes)
    while len(q)!=0: # if there is still something in the queue to look at, I can keep going.
        tmpPath = q.pop(0)
    return None # if theres nothing in the queue anymore
#from graph import *
#
def BFS(graph, start, end, q = []):
    initPath = [start]
    q.append(initPath)
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
        print 'Current dequeued path:', printPath(tmpPath)
        if lastNode == end:
            return tmpPath
        for linkNode in graph.childrenOf(lastNode):
            if linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
    return None