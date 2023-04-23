from BucketList import bucket_list
import coverage
import random
import numpy as np
import time


def evaluate(x, n_parameters):

    cov = coverage.Coverage(branch=True)
    cov.start()

    for i in range(len(x)):
        if x[i, 6] == 1:
            bucket_list(x[i, 0], x[i, 1], x[i, 2], x[i, 3], x[i, 4], x[i, 5])

    cov.stop()
    data = cov.get_data()

    lines_covered = sum(len(data.lines(filename)) for filename in data.measured_files())
    branches_covered = sum(len(data.arcs(filename)) for filename in data.measured_files())
    n_cases_used = np.sum(x[:, n_parameters])

    return lines_covered, branches_covered, n_cases_used

def random_population(n_cases, n_parameters, lower_bound, upper_bound):
    x = []
    for i in range(n_cases):
        random_individual = [random.randint(lower_bound[j], upper_bound[j]) for j in range(n_parameters)]
        random_individual.append(random.randint(0, 1))
        x.append(random_individual)
    return np.array(x)

start_time = time.time()

n_cases = 50
n_parameters = 6
lower_bound = [1, 1, 1, 1, 1, 1]
upper_bound = [1500, 1500, 1500, 1500, 1500, 1500]

best_lines = 0
best_branches = 0
best_n_cases = 50

for _ in range(2500):
    x = random_population(n_cases, n_parameters, lower_bound, upper_bound)
    line, branch, cases = evaluate(x, n_parameters)
    if line >= best_lines and branch >= best_branches and cases <= best_n_cases:
        best_lines = line
        best_branches = branch
        best_n_cases = cases

end_time = time.time()

print("best lines: ", best_lines)
print("best branches: ", best_branches)
print("best num of cases: ", best_n_cases)
print("Time elapsed: ", end_time - start_time, "seconds")
