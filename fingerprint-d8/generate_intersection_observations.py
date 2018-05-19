import networkx

def generate_intersection_observations(graph, num_tsteps):
  # Collect honest and spy IDs
  hon_ids = []
  spy_ids = []
  for node_id in list(graph.nodes()):
    if graph.node[node_id]['is_spy']:
      spy_ids.append(node_id)
    else:
      hon_ids.append(node_id)
  # Construct empty observations structure: {hon_id: {spy_id: {inf_id: prob}}}
  observations = {}
  for hon_id in hon_ids:
    observations[hon_id] = {}
    for spy_id in spy_ids:
      observations[hon_id][spy_id] = {}
      inf_ids = list(graph.predecessors(spy_id))
      for inf_id in inf_ids:
        observations[hon_id][spy_id][inf_id] = 0.0
  # Run num_tsteps of diffusion observations
  for tstep in range(num_tsteps):
    adobs = generate_diffusion_observations(graph)
    for spy_key in adobs:
      for inf_key in adobs[spy_key]:
        for node_id in adobs[spy_key][inf_key]:
          observations[node_id][spy_key][inf_key]+=1.0
  # Normalize
  for node_key in observations:
    for spy_key in observations[node_key]:
      for inf_key in observations[node_key][spy_key]:
        observations[node_key][spy_key][inf_key]/=float(num_tsteps)
  # Return
  return observations
