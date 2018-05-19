import math
import networkx

def generate_max_weight_matching_with_routes(graph, d, adversary_observations, one_to_one_maps):
  # Collect list of spy IDs
  spy_ids = []
  for node_id in list(graph.nodes()):
    if graph.node[node_id]['is_spy']:
      spy_ids.append(node_id)
  # Construct honest graph subgraph of graph
  honest_graph = graph.copy()
  honest_graph.remove_nodes_from(spy_ids)
  # Initialize bipartite graph
  bipartite_graph = networkx.Graph()
  # Build left side of bipartite graph, the honest/originator nodes
  b_node_id=0
  b_originator_ids = []
  for originator_id in list(honest_graph.nodes()):
    bipartite_graph.add_node(b_node_id, originator=originator_id)
    b_originator_ids.append(b_node_id)
    b_node_id+=1
  # Build right side of bipartite graph, the messages
  # Fully connect the two sides of the bipartite graph with edges weights 0.0
  b_message_ids = []
  for spy_id in adversary_observations:
    for informer_id in adversary_observations[spy_id]:
      message_id=0
      while message_id<len(adversary_observations[spy_id][informer_id]):
        bipartite_graph.add_node(b_node_id, spy=spy_id, informer=informer_id, message=message_id)
        b_message_ids.append(b_node_id)
        b_node_id+=1
        message_id+=1
        for b_originator_id in b_originator_ids:
          bipartite_graph.add_edge(b_originator_id, b_message_ids[-1], weight=0.0)
  # Calculate and update the edge weights
  max_path_len = graph.number_of_nodes()
  for orig_id in b_originator_ids:
    honest_node_id = bipartite_graph.node[orig_id]['originator']
    orig_id_map = {}
    for k in one_to_one_maps[honest_node_id]:
      orig_id_map[k] = one_to_one_maps[honest_node_id][k]
    if len(orig_id_map)>1:
      del orig_id_map[honest_node_id]
    d_prob = 1.0/float(len(orig_id_map))
    for pred_id in orig_id_map:
      prev_loc = honest_node_id
      curr_loc = orig_id_map[pred_id]
      path_len = 1
      while (curr_loc not in spy_ids) and (path_len < max_path_len):
        next_loc = one_to_one_maps[curr_loc][prev_loc]
        prev_loc = curr_loc
        curr_loc = next_loc
        path_len+=1
      if curr_loc in spy_ids:
        vs = []
        for v in b_message_ids:
          if bipartite_graph.node[v]['spy']==curr_loc and bipartite_graph.node[v]['informer']==prev_loc:
            vs.append(v)
        m_prob = 0.0
        if len(vs)>0:
          m_prob = 1.0/float(len(vs))
        for v in vs:
          bipartite_graph.edges[orig_id,v]['weight']+=d_prob*m_prob
      else:
        vs = b_message_ids
        m_prob = 0.0
        if len(vs)>0:
          m_prob = 1.0/float(len(vs))
        for v in vs:
          bipartite_graph.edges[orig_id,v]['weight']+=d_prob*m_prob
  # Determine max weight matching
  raw_matching = networkx.max_weight_matching(bipartite_graph, maxcardinality=True)
  # Convert to returnable version
  max_weight_matching = {}
  for b_originator_id in b_originator_ids:
    spy_id = bipartite_graph.nodes[raw_matching[b_originator_id]]['spy']
    informer_id = bipartite_graph.nodes[raw_matching[b_originator_id]]['informer']
    if spy_id not in max_weight_matching:
      max_weight_matching[spy_id] = {}
    if informer_id not in max_weight_matching[spy_id]:
      max_weight_matching[spy_id][informer_id] = []
    max_weight_matching[spy_id][informer_id].append(bipartite_graph.nodes[b_originator_id]['originator'])
  return max_weight_matching
