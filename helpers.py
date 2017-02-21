
def displacement_stub(nodes):
    '''
    displaces water between two nodes as follows:
    half of the difference in water height * the average param_stub
    '''
    node1 = nodes[0]
    node2 = nodes[1]
    height1 = node1.get_height()
    height2 = node2.get_height()
#     node_receiver = None
#     node_releaser = None
    if abs(height1-height2)<0.00005:
        return None
    elif height1<height2:
        node_receiver = node1
        node_releaser = node2
    else:
        node_receiver = node2
        node_releaser = node1
    displacement_quantity = abs(height1-height2)/2*(node1.get_stub_param()+node2.get_stub_param())/2        
    node_receiver.increase_height(displacement_quantity)
    node_releaser.decrease_height(displacement_quantity)
    
