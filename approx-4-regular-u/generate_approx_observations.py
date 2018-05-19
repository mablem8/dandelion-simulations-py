import networkx
import random

def generate_approx_observations(graph, one_to_one_maps):
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
  for node_id in list(graph.nodes()):
    if node_id not in spy_ids:
      prev_msg_location = node_id
      curr_msg_location = one_to_one_maps[node_id][node_id]
      path_length=1
      while (curr_msg_location not in spy_ids) and (path_length<max_path_length):
        next_msg_location = one_to_one_maps[curr_msg_location][prev_msg_location]
        prev_msg_location = curr_msg_location
        curr_msg_location = next_msg_location
        path_length+=1
      if curr_msg_location in spy_ids:
        adversary_observations[curr_msg_location][prev_msg_location].append(node_id)
      else:
        rand_spy_id = random.sample(spy_ids, 1)[0]
        rand_informer_id = -1
        if len(list(graph.predecessors(rand_spy_id))) > 0:
          rand_informer_id = random.sample(list(graph.predecessors(rand_spy_id)), 1)[0]
        while (rand_informer_id == -1) or (rand_informer_id in spy_ids):
          rand_spy_id = random.sample(spy_ids, 1)[0]
          rand_informer_id = -1
          if len(list(graph.predecessors(rand_spy_id))) > 0:
            rand_informer_id = random.sample(list(graph.predecessors(rand_spy_id)), 1)[0]
        adversary_observations[rand_spy_id][rand_informer_id].append(node_id)
  return adversary_observations
