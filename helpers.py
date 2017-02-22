
def displacement_stub(edges):
    '''
    displaces water between any number of edges as follows:
    difference between the average height and the height of each edge * the average param_stub
    '''
    
    average_height = 0
    average_stub_param = 0
    edge_count  = 0 
    for edge in edges:
        edge_count += 1
        average_height += edge.get_height()
        average_stub_param += edge.get_stub_param()
    average_height /= edge_count 
    average_stub_param /= edge_count
    
    for edge in edges:
        height = edge.get_height()
        displacement_quantity = average_height-height
        if abs(displacement_quantity)<0.00005:
            pass
        else:
            edge.adjust_height(displacement_quantity*average_stub_param)
