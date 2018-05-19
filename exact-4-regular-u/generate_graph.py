import math
import networkx
import random

def generate_graph(n,p,d):
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
    candidate_successor_ids = random.sample(list(graph.nodes()), networkx.DiGraph.number_of_nodes(graph))
    i=0
    while graph.out_degree(node_id)<d and i<len(candidate_successor_ids):
      if node_id!=candidate_successor_ids[i] and graph.in_degree(candidate_successor_ids[i])<d:
        graph.add_edge(node_id, candidate_successor_ids[i])
      i+=1
  # Patch missing in and out degrees
  lost_in_degree_ids = []
  full_in_degree_ids = []
  for node_id in list(graph.nodes()):
    if graph.in_degree(node_id)<d:
      lost_in_degree_ids.append(node_id)
    elif graph.in_degree(node_id)==d:
      full_in_degree_ids.append(node_id)
    else:
      raise Exception('In degree too large')
  lost_in_degree_ids = random.sample(lost_in_degree_ids, len(lost_in_degree_ids))
  lost_outdegree_ids = []
  full_outdegree_ids = []
  for node_id in list(graph.nodes()):
    if graph.out_degree(node_id)<d:
      lost_outdegree_ids.append(node_id)
    elif graph.out_degree(node_id)==d:
      full_outdegree_ids.append(node_id)
    else:
      raise Exception('Out degree too large')
  lost_outdegree_ids = random.sample(lost_outdegree_ids, len(lost_outdegree_ids))
  if len(lost_in_degree_ids)!=len(lost_outdegree_ids):
    raise Exception('Number of missing in and out degrees do not match')
  for i in range(len(lost_in_degree_ids)):
    full_in_degree_ids = random.sample(full_in_degree_ids, len(full_in_degree_ids))
    full_outdegree_ids = random.sample(full_outdegree_ids, len(full_outdegree_ids))
    lost_in_degree_id = lost_in_degree_ids[i]
    lost_outdegree_id = lost_outdegree_ids[i]
    # Find appropriate (full_outdegree_id, full_in_degree_id) pair
    full_in_degree_id = -1
    full_outdegree_id = -1
    for fod_id in full_outdegree_ids:
      if fod_id!=lost_in_degree_id:
        suc_ids = list(graph.successors(fod_id))
        for suc_id in suc_ids:
          if (suc_id in full_in_degree_ids) and (suc_id!=lost_outdegree_id):
            full_in_degree_id = suc_id
            full_outdegree_id = fod_id
            break
        if full_in_degree_id!=-1 and full_outdegree_id!=-1:
          break
    # Patch
    graph.remove_edge(full_outdegree_id, full_in_degree_id)
    graph.add_edge(full_outdegree_id, lost_in_degree_id)
    graph.add_edge(lost_outdegree_id, full_in_degree_id)
  return graph
