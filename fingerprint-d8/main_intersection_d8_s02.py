exec(open('./generate_approx_graph.py').read())
exec(open('./generate_diffusion_observations.py').read())
exec(open('./generate_intersection_observations.py').read())
exec(open('./generate_intersection_signatures.py').read())
exec(open('./calculate_max_weight_matching_intersection_precision.py').read())

n=100
d=8
ps=[0.20,0.25,0.30,0.35,0.40,0.45,0.50]
num_trials=256
header=['Fraction of Spies']
for trial in range(num_trials):
  header.append('Trial '+str(trial)+' Precision')

import csv
with open('data-intersection-d8-s02.csv', 'w', newline='') as csvfile:
  datawriter = csv.writer(csvfile, delimiter=',')
  datawriter.writerow(header)

results=[]
for p in ps:
  results.append([str(p)])
  for trial in range(num_trials):
    graph = generate_approx_graph(n,p,d)
    adobs = generate_intersection_observations(graph, 2)
    sgntr = generate_intersection_signatures(graph, 1000)
    prcsn = calculate_max_weight_matching_intersection_precision(graph, adobs, sgntr)
    results[-1].append(str(prcsn))
  with open('data-intersection-d8-s02.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')
    datawriter.writerow(results[-1])
