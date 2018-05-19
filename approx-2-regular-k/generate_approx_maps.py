import networkx
import random

def generate_approx_maps(graph):
  approx_maps = {}
  for node_id in list(graph.nodes()):
    predecessor_ids = list(graph.predecessors(node_id))
    successor_ids = list(graph.successors(node_id))
    destination_ids = []
    # Cases: # predecessors < # successors, # predecessors = # successors
    if len(predecessor_ids) <= len(successor_ids):
      destination_ids = random.sample(successor_ids, len(predecessor_ids))
    # Case: # predecessors > # successors
    else:
      # Since # predecessors > # successors, all of the successors are used
      destination_ids = random.sample(successor_ids, len(successor_ids))
      # Close the gap to less than the number of successors
      while (len(predecessor_ids)-len(destination_ids)) >= len(successor_ids):
        more_destination_ids = random.sample(successor_ids, len(successor_ids))
        for destination_id in more_destination_ids:
          destination_ids.append(destination_id)
      # If a gap remains, it can be filled exactly with a subset of successors
      if len(predecessor_ids) > len(destination_ids):
        gap = len(predecessor_ids) - len(destination_ids)
        more_destination_ids = random.sample(successor_ids, gap)
        for destination_id in more_destination_ids:
          destination_ids.append(destination_id)
    # Add destination for locally generated message
    predecessor_ids.append(node_id)
    if len(destination_ids)>0:
      destination_ids.append(random.sample(destination_ids, 1)[0])
    else:
      destination_ids.append(random.sample(successor_ids, 1)[0])
    if len(predecessor_ids)!=len(destination_ids):
      raise Exception('In and out degrees are different')
    approx_maps[node_id] = dict(zip(predecessor_ids, destination_ids))
  return approx_maps
