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


