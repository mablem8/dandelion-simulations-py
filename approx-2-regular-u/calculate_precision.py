import random

def calculate_precision(adversary_observations, max_weight_matching):
  recall = 0.0
  total = 0.0
  for spy_id in max_weight_matching:
    for informer_id in max_weight_matching[spy_id]:
      max_weight_matching[spy_id][informer_id] = random.sample(max_weight_matching[spy_id][informer_id], len(max_weight_matching[spy_id][informer_id]))
      for originator_id_index in range(len(max_weight_matching[spy_id][informer_id])):
        if max_weight_matching[spy_id][informer_id][originator_id_index]==adversary_observations[spy_id][informer_id][originator_id_index]:
          recall+=1.0
        total+=1.0
  return recall/total
