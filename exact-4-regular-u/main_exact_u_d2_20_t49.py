exec(open('./generate_graph.py').read())
exec(open('./regularize_graph.py').read())
exec(open('./generate_one_to_one_maps.py').read())
exec(open('./generate_adversary_observations.py').read())
exec(open('./generate_max_weight_matching.py').read())
exec(open('./calculate_precision.py').read())

n=100
d=2
ps=[0.20]
num_trials=1
header=['Fraction of Spies']
for trial in range(num_trials):
  header.append('Trial '+str(trial)+' Precision')

import csv
with open('data-exact-u-d2-20-t49.csv', 'w', newline='') as csvfile:
  datawriter = csv.writer(csvfile, delimiter=',')
  datawriter.writerow(header)

results=[]
for p in ps:
  results.append([str(p)])
  for trial in range(num_trials):
    graph = generate_graph(n,p,d)
    graph = regularize_graph(graph,d)
    o2omp = generate_one_to_one_maps(graph)
    adobs = generate_adversary_observations(graph, o2omp)
    mwmat = generate_max_weight_matching(graph, d, adobs)
    prcsn = calculate_precision(adobs, mwmat)
    results[-1].append(str(prcsn))
  with open('data-exact-u-d2-20-t49.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')
    datawriter.writerow(results[-1])
