import math
import networkx
import random

def generate_approx_graph(n,p,d):
  graph = networkx.DiGraph()
  # Populate graph with nodes
  spy_ids = random.sample(range(n), int(math.floor(p*n)))
  for node_id in range(n):
    if node_id in spy_ids:
      graph.add_node(node_id, is_spy=True)
    else:
      graph.add_node(node_id, is_spy=False)
  # Populate graph with edges
  for node_id in list(graph.nodes()):
    successor_ids = random.sample(list(graph.nodes()), d)
    for successor_id in successor_ids:
      graph.add_edge(node_id, successor_id)
  return graph
