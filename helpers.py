
def displacement_stub(edges):
    '''
    displaces water between any number of edges as follows:
    difference between the average height and the height of each edge * the average param_stub
    '''
    
    average_volume = 0
    average_stub_param = 0
    edge_count  = 0 
    for edge in edges:
        edge_count += 1
        average_volume += edge.get_water_volume()
        average_stub_param += edge.get_stub_param()
    average_volume /= edge_count 
    average_stub_param /= edge_count
    
    for edge in edges:
        volume = edge.get_water_volume()
        displacement_quantity = average_volume-volume
        if abs(displacement_quantity)<0.00005:
            pass
        else:
            edge.adjust_water_volume(displacement_quantity*average_stub_param)

def edge_flow_stub(end_node_unknown_flow):
    displacement_quantity = 0
    height_difference = 0
    edge = end_node_unknown_flow.get_edges()[0]
    edge_height=edge.get_water_level()
    edge_volume_height_ratio = edge.get_height_volume_ratio()
    threshold = end_node_unknown_flow.get_threshold()

    if edge_height<threshold:
        pass
    else:
        height_difference = edge_height-threshold
        displacement_quantity = height_difference/edge_volume_height_ratio*-1
        edge.adjust_water_volume(displacement_quantity)
        