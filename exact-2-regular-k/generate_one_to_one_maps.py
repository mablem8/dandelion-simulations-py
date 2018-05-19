import networkx
import random

def generate_one_to_one_maps(graph):
  one_to_one_maps = {}
  for node_id in list(graph.nodes()):
    predecessor_ids = list(graph.predecessors(node_id))
    predecessor_ids.append(node_id)
    successor_ids = list(graph.successors(node_id))
    destination_ids = random.sample(successor_ids, len(successor_ids))
    destination_ids.append(random.sample(successor_ids, 1)[0])
    if len(predecessor_ids)!=len(destination_ids):
      raise Exception('In and out degrees are different')
    else:
      one_to_one_maps[node_id] = dict(zip(predecessor_ids, destination_ids))
    #one_to_one_maps[node_id] = dict(zip(predecessor_ids, destination_ids))
  return one_to_one_maps
