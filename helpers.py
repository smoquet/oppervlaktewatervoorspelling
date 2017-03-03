def edge_water_level_is_lower(edge, water_level):
    return edge.get_water_level() < water_level

def get_average_water_level(edges):    
    total_water_level = 0.0
    for edge in edges:
        total_water_level += edge.get_water_level()        
    return total_water_level / len(edges)




#DEBUG STATEMT:# water_receiving_edges[0].get_nodes()[0].graph.get_total_water_in_system()
def discharge_q_accordingly(discharge_Q_to_be_transferred,
                            average_water_level,
                            water_receiving_edges, 
                            water_giving_edges,
                            total_discharge_Q_of_receivers_of_water,
                            total_discharge_Q_of_givers_of_water,
                            overload_corrected_discharge,
                            calculation_mode
                            ):
    ''' recursive function that calculates the correct discharge
    this function is recursive, because manning's formula often
    discharges to much, and the edges of this node start oscillating endlessly. 
    This function reduces the discharge if needed, based on a calculation of the Q_overload,
    it then corrects for this, while keeping track of what the discharge should have been. 
    It then returns the corrected discharge 
    '''
         
    Q_overload = 0.0
    temp_Q_overload = 0.0
    overload_ratio = 0.0
    for receiver in water_receiving_edges:
        discharge_ratio = receiver.get_discharge_Q()/total_discharge_Q_of_receivers_of_water
        Q_to_give_to_this_receiving_edge = discharge_Q_to_be_transferred*discharge_ratio
        receiver.adjust_water_volume(Q_to_give_to_this_receiving_edge)
         
#             if receiver.get_water_level()-average_water_level <0.000000001 :  # water is overloading, this will create endless oscillation
        if receiver.get_water_level() > average_water_level:  # water is overloading, this will create endless oscillation
            temp_Q_overload = receiver.calculate_surplus_Q(average_water_level)  # get amount of surplus Q, and the discharge ratio
            if Q_overload < temp_Q_overload:
                Q_overload = temp_Q_overload  # keep track of largest surplus Q
    for giver in water_giving_edges:
        discharge_ratio = giver.get_discharge_Q()/total_discharge_Q_of_givers_of_water
        Q_to_be_reduced = -1* discharge_Q_to_be_transferred * discharge_ratio
        giver.adjust_water_volume(Q_to_be_reduced)
             
    overload_corrected_discharge += discharge_Q_to_be_transferred
     
    if Q_overload > 0.0001 and calculation_mode:  # overload of Q 
        overload_corrected_discharge = discharge_q_accordingly(-1.0*Q_overload, 
                        average_water_level, 
                        water_receiving_edges, 
                        water_giving_edges,
                        total_discharge_Q_of_receivers_of_water,
                        total_discharge_Q_of_givers_of_water,
                        overload_corrected_discharge,
                        calculation_mode
                        )
    return overload_corrected_discharge

def displace_water_between_edges(node):
    '''expects: an instance of a node
    1: get average_water_level from edges to decide the height of the node 
    2: set slopes of edges according to this average height, their lengths and water level 
    3: get all the Q's from each edge, calculate the average
    4: call on function discharge_q_accrodingly to 
        1) first calculate the correct discharge
        2) use this discharge to correctly transfer water with the same function
    '''
    Q_overload = 0.0
    edges = node.get_edges()
    water_receiving_edges = []
    water_giving_edges = []
    added_lower_water_levels = 0.0
    total_discharge_Q_of_receivers_of_water = 0.0
    total_discharge_Q_of_givers_of_water = 0.0
    total_discharge_Q_of_all_nodes = 0.0
    average_water_level = get_average_water_level(edges)  #part1
    
    for edge in edges:  #part2+3
        slope = edge.calculate_set_and_return_slope_and_calculate_discharge(average_water_level)
        total_discharge_Q_of_all_nodes += edge.get_discharge_Q()
        if slope == 0.0 or slope < 0.000000000001:
            water_receiving_edges.append(edge)
        elif not edge_water_level_is_lower(edge, average_water_level):  #giver of water
            edge.update_water_direction(node)  
            water_giving_edges.append(edge)
            total_discharge_Q_of_givers_of_water += edge.get_discharge_Q()  
        elif edge_water_level_is_lower(edge, average_water_level):  #receiver of water
            water_receiving_edges.append(edge)
            total_discharge_Q_of_receivers_of_water += edge.get_discharge_Q()
    
    total_discharge_Q_of_all_nodes = total_discharge_Q_of_givers_of_water + total_discharge_Q_of_receivers_of_water
    proposed_discharge_Q_to_be_transferred = abs(total_discharge_Q_of_all_nodes/len(edges))  #average_discharge
    
    if proposed_discharge_Q_to_be_transferred != 0.0:  #part4
        corrected_discharge = discharge_q_accordingly(proposed_discharge_Q_to_be_transferred, average_water_level, 
                                water_receiving_edges, water_giving_edges,
                                total_discharge_Q_of_receivers_of_water, 
                                total_discharge_Q_of_givers_of_water,
                                overload_corrected_discharge=0,
                                calculation_mode = True
                                )
        
        discharge_q_accordingly(corrected_discharge, average_water_level, 
                                water_receiving_edges, water_giving_edges,
                                total_discharge_Q_of_receivers_of_water, 
                                total_discharge_Q_of_givers_of_water,
                                overload_corrected_discharge=0,
                                calculation_mode = False
                                )
    
def weir_displace_water_between_edges(weir):
    ''' displaces water between two edges of the weir
    expects a weir with two edges, one of which has a higher water_level_than the height of the weir,
    the other has a lower level
    '''
    
    height_difference = 0.0
    discharge_Q = 0.0
    for edge in weir.get_edges():
        height_difference = edge.get_water_level() - weir.height
        if height_difference > 0: #this means this edge is the giver of water
            edge.update_water_direction(weir) # this weir is the direction in which the water went from this edge
            discharge_Q = weir.weir_constant * weir.width * height_difference**1.5
            edge.adjust_water_volume(-1.0*discharge_Q) # reduce Q of giver
            weir.get_other_edge(edge).adjust_water_volume(discharge_Q,) # add Q to receiver
            