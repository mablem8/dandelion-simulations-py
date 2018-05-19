import math
import networkx

def calculate_max_weight_matching_intersection_precision(graph, intersection_observations, intersection_signatures):
  # Construct dictionary of observation vectors
  obs = {}
  for hon_id in intersection_observations:
    obs[hon_id] = []
    for spy_id in intersection_observations[hon_id]:
      for inf_id in intersection_observations[hon_id][spy_id]:
        obs[hon_id].append(intersection_observations[hon_id][spy_id][inf_id])
  # Construct dictionary of signatures vectors
  sig = {}
  for hon_id in intersection_signatures:
    sig[hon_id] = []
    for spy_id in intersection_signatures[hon_id]:
      for inf_id in intersection_signatures[hon_id][spy_id]:
        sig[hon_id].append(intersection_signatures[hon_id][spy_id][inf_id])
  # Initialize bipartite graph
  bipartite_graph = networkx.Graph()
  # Build left side of bipartite graph, the observation vectors
  b_node_id=0
  b_obs_ids = []
  for obs_id in obs:
    bipartite_graph.add_node(b_node_id, obs=obs_id)
    b_obs_ids.append(b_node_id)
    b_node_id+=1
  # Build right side of bipartite graph, the signature vectors
  b_sig_ids = []
  for sig_id in sig:
    bipartite_graph.add_node(b_node_id, sig=sig_id)
    b_sig_ids.append(b_node_id)
    b_node_id+=1
  # Fully connect the two sides with appropriate edge weights
  for b_obs_id in b_obs_ids:
    for b_sig_id in b_sig_ids:
      obs_vec = obs[bipartite_graph.nodes[b_obs_id]['obs']]
      sig_vec = sig[bipartite_graph.nodes[b_sig_id]['sig']]
      if len(obs_vec) != len(sig_vec):
        raise AssertionError("Obs and Sig vector lengths do not match")
      dist = 0.0
      for i in range(len(obs_vec)):
        dist += math.pow(obs_vec[i]-sig_vec[i],2.0)
      dist = math.sqrt(dist)
      max_metric = math.sqrt(len(obs_vec)) - dist
      bipartite_graph.add_edge(b_obs_id, b_sig_id, weight=max_metric)
  # Determine max weight matching
  raw_matching = networkx.max_weight_matching(bipartite_graph, maxcardinality=True)
  # Calculate precision
  recall = 0.0
  total = 0.0
  for b_obs_id in b_obs_ids:
    if bipartite_graph.nodes[b_obs_id]['obs'] == bipartite_graph.nodes[raw_matching[b_obs_id]]['sig']:
      recall += 1.0
    total += 1.0
  return recall/total
