exec(open('./generate_approx_graph.py').read())
exec(open('./generate_approx_maps.py').read())
exec(open('./generate_approx_observations.py').read())
exec(open('./generate_max_weight_matching_with_routes.py').read())
exec(open('./calculate_precision.py').read())

n=100
d=1
ps=[0.20,0.25,0.30,0.35,0.40,0.45,0.50]
num_trials=256
header=['Fraction of Spies']
for trial in range(num_trials):
  header.append('Trial '+str(trial)+' Precision')

import csv
with open('data-approx-k-d1.csv', 'w', newline='') as csvfile:
  datawriter = csv.writer(csvfile, delimiter=',')
  datawriter.writerow(header)

results=[]
for p in ps:
  results.append([str(p)])
  for trial in range(num_trials):
    graph = generate_approx_graph(n,p,d)
    o2omp = generate_approx_maps(graph)
    adobs = generate_approx_observations(graph, o2omp)
    mwmat = generate_max_weight_matching_with_routes(graph, d, adobs, o2omp)
    prcsn = calculate_precision(adobs, mwmat)
    results[-1].append(str(prcsn))
  with open('data-approx-k-d1.csv', 'a', newline='') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',')
    datawriter.writerow(results[-1])
