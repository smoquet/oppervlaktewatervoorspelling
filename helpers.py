def edge_water_level_is_lower(edge, water_level):
    return edge.get_water_level() < water_level

def displace_water_between_edges(edges):
    '''expects: edges that are connected with each other
    1: get average_water_level from edges
    2: set slopes of edges according to this average height, their heights and lengths
    3: get Q from edges that are net givers of water, and subtract this amount from their water_volume
    4: give the Q to the net receiving edges on the ratio of their respective slopes (the most sloped ones get more)
    returns nothing 
    '''
    average_water_level = 0.0
#     edges_dict = {}
    water_receiving_edges = []
    total_Q_to_give_to_receiving_edges = 0.0
    added_lower_water_levels = 0.0
    for edge in edges:
        edge_water_level = edge.get_water_level()
        average_water_level += edge_water_level
#         edges_dict[edge] = [edge_water_level]
    average_water_level /= len(edges)
    for edge in edges:
        slope = edge.calculate_set_and_return_slope_and_calculate_discharge(average_water_level)
#         edges_dict[edge].append(slope) 
        if slope == 0.0:
            water_receiving_edges.append([edge, 0]) 
        elif not edge_water_level_is_lower(edge, average_water_level): # giver of water
            water_displacement_quantity = edge.get_discharge_Q()
            total_Q_to_give_to_receiving_edges +=water_displacement_quantity 
            edge.adjust_water_volume(-1*abs(water_displacement_quantity))
        elif edge_water_level_is_lower(edge, average_water_level): # receiver of wter
            edge_water_level = edge.get_water_level()
            difference_in_water_level = average_water_level-edge_water_level
            added_lower_water_levels += difference_in_water_level
            water_receiving_edges.append([edge, difference_in_water_level])
    for receivers in water_receiving_edges:
        edge = receivers[0]
        difference_in_water_level = receivers[1]
        ratio_of_total_Q_to_be_given_to_this_edge = difference_in_water_level/added_lower_water_levels
        Q_to_give_to__this_receiving_edge = total_Q_to_give_to_receiving_edges*ratio_of_total_Q_to_be_given_to_this_edge
        edge.adjust_water_volume(Q_to_give_to__this_receiving_edge)
        

# def edge_flow_stub(end_node_unknown_flow):
#     displacement_quantity = 0
#     height_difference = 0
#     edge = end_node_unknown_flow.get_edges()[0]
#     edge_height=edge.get_water_level()
#     edge_volume_height_ratio = edge.get_height_volume_ratio()
#     threshold = end_node_unknown_flow.get_threshold()
#  
#     if edge_height<threshold:
#         pass
#     else:
#         height_difference = edge_height-threshold
#         displacement_quantity = height_difference/edge_volume_height_ratio*-1
#         edge.adjust_water_volume(displacement_quantity)

def edge_flow_stub(end_node_unknown_flow):
    node_has_higher_level_than_threshold = end_node_unknown_flow.water_level < end_node_unknown_flow.threshold
    edge_water_level = end_node_unknown_flow.edges[0].get_water_level()
    edge_has_higher_level_than_threshold = edge_water_level > end_node_unknown_flow.threshold
     
    if not node_has_higher_level_than_threshold and not edge_has_higher_level_than_threshold:
        pass # both levels are to low for movement
    elif node_has_higher_level_than_threshold and not edge_has_higher_level_than_threshold:
        # node gives water to edge
        water_level_difference = end_node_unknown_flow.water_level-end_node_unknown_flow.threshold
        displacement_quantity = end_node_unknown_flow.qh_relationship(h=water_level_difference)
        end_node_unknown_flow.edges[0].adjust_water_volume(-1*displacement_quantity)
    elif not node_has_higher_level_than_threshold and edge_has_higher_level_than_threshold:
        # edge gives water to node
        water_level_difference = edge_water_level-end_node_unknown_flow.threshold
        displacement_quantity = end_node_unknown_flow.qh_relationship(h=water_level_difference)
        end_node_unknown_flow.edges[0].adjust_water_volume(displacement_quantity)
    else:
        #both are higher than threshold, the difference between two hights dictates the direction and q
        water_level_difference = end_node_unknown_flow.water_level-edge_water_level
        displacement_quantity = end_node_unknown_flow.qh_relationship(water_level_difference)
        end_node_unknown_flow.edges[0].adjust_water_volume(displacement_quantity)

def qh_relationship_end_node_unknown_flow_1(Q = None, h=None):
    if not Q and not h:
        raise StandardError('No Q or h passed on to Qh-function')
    elif Q and h:
        raise StandardError('Both Q and h passed on to Qh-function')
    elif Q and not h:
        h = Q*0.5 # voor elke Q krijg je 0.5 h
        return h
    else:
        Q = h/0.5 # voor elke h krijg je 2 Q
        return Q

    
    