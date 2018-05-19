import networkx
import random

def generate_diffusion_observations(graph):
  spy_ids = []
  for node_id in list(graph.nodes()):
    if graph.node[node_id]['is_spy']:
      spy_ids.append(node_id)
  adversary_observations = {}
  for spy_id in spy_ids:
    if spy_id not in adversary_observations:
      adversary_observations[spy_id] = {}
    informer_ids = list(graph.predecessors(spy_id))
    for informer_id in informer_ids:
      if informer_id not in adversary_observations[spy_id]:
        adversary_observations[spy_id][informer_id] = []
  max_path_length = graph.number_of_nodes()
  honest_graph = graph.copy()
  honest_graph.remove_nodes_from(spy_ids)
  for node_id in list(honest_graph.nodes()):
    prev_loc = node_id
    curr_loc = random.sample(list(graph.successors(node_id)), 1)[0]
    path_len = 1
    while (curr_loc not in spy_ids) and (path_len < max_path_length):
      next_loc = random.sample(list(graph.successors(curr_loc)), 1)[0]
      prev_loc = curr_loc
      curr_loc = next_loc
      path_len+=1
    if curr_loc in spy_ids:
      adversary_observations[curr_loc][prev_loc].append(node_id)
    else:
      rand_spy = random.sample(spy_ids, 1)[0]
      rand_inf = -1
      if len(list(graph.predecessors(rand_spy))) > 0:
        rand_inf = random.sample(list(graph.predecessors(rand_spy)), 1)[0]
      while (rand_inf == -1) or (rand_inf in spy_ids):
        rand_spy = random.sample(spy_ids, 1)[0]
        rand_inf = -1
        if len(list(graph.predecessors(rand_spy))) > 0:
          rand_inf = random.sample(list(graph.predecessors(rand_spy)), 1)[0]
      adversary_observations[rand_spy][rand_inf].append(node_id)
  return adversary_observations
