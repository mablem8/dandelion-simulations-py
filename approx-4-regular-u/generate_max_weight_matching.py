import math
import networkx

def generate_max_weight_matching(graph, d, adversary_observations):
  spy_ids = []
  for node_id in list(graph.nodes()):
    if graph.node[node_id]['is_spy']:
      spy_ids.append(node_id)
  honest_graph = graph.copy()
  honest_graph.remove_nodes_from(spy_ids)
  bipartite_graph = networkx.Graph()
  b_node_id=0
  b_originator_ids = []
  for originator_id in list(honest_graph.nodes()):
    bipartite_graph.add_node(b_node_id, originator=originator_id)
    b_originator_ids.append(b_node_id)
    b_node_id+=1
  base=1.0/float(d)
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
          gen_paths = networkx.all_simple_paths(honest_graph, source=bipartite_graph.nodes[b_originator_id]['originator'], target=informer_id)
          paths = []
          for p in gen_paths:
            paths.append(p)
          if bipartite_graph.nodes[b_originator_id]['originator']==informer_id:
            paths.append([informer_id])
          wt = 0.0
          for path in paths:
            wt+=math.pow(base,len(path))
          bipartite_graph.add_edge(b_originator_id, b_message_ids[-1], weight=wt)
  raw_matching = networkx.max_weight_matching(bipartite_graph, maxcardinality=True)
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
