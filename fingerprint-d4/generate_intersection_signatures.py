import networkx

def generate_intersection_signatures(graph, num_trials):
  # Collect honest and spy IDs
  hon_ids = []
  spy_ids = []
  for node_id in list(graph.nodes()):
    if graph.node[node_id]['is_spy']:
      spy_ids.append(node_id)
    else:
      hon_ids.append(node_id)
  # Construct empty signatures structure: {hon_id: {spy_id: {inf_id: prob}}}
  signatures = {}
  for hon_id in hon_ids:
    signatures[hon_id] = {}
    for spy_id in spy_ids:
      signatures[hon_id][spy_id] = {}
      inf_ids = list(graph.predecessors(spy_id))
      for inf_id in inf_ids:
        signatures[hon_id][spy_id][inf_id] = 0.0
  # Run num_trials of diffusion observations
  for trial in range(num_trials):
    adobs = generate_diffusion_observations(graph)
    for spy_key in adobs:
      for inf_key in adobs[spy_key]:
        for node_id in adobs[spy_key][inf_key]:
          signatures[node_id][spy_key][inf_key]+=1.0
  # Normalize
  for node_key in signatures:
    for spy_key in signatures[node_key]:
      for inf_key in signatures[node_key][spy_key]:
        signatures[node_key][spy_key][inf_key]/=float(num_trials)
  # Return
  return signatures
