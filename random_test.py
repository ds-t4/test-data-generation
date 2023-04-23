from BucketList import bucket_list
import coverage
import random
import numpy as np
import time


def evaluate(x):
    # print('evaluating', x)

    cov = coverage.Coverage(branch=True)

    cov.start()

    for i in range(len(x)):
        bucket_list(x[i, 0], x[i, 1], x[i, 2], x[i, 3], x[i, 4], x[i, 5])

    cov.stop()
    data = cov.get_data()

    lines_covered = sum(len(data.lines(filename)) for filename in data.measured_files())
    # print(f"Line covered: {lines_covered}")

    branches_covered = sum(len(data.arcs(filename)) for filename in data.measured_files())
    # print(f"Branches coverage: {branches_covered}")

    return lines_covered, branches_covered

def random_population(pop_size, n_parameters, lower_bound, upper_bound):
    x = []

    for i in range(pop_size):
        random_individual = [random.randint(lower_bound[j], upper_bound[j]) for j in range(n_parameters)]
        x.append(random_individual)
    return np.array(x)

start_time = time.time()

pop_size = 30
n_parameters = 6
lower_bound = [1, 1, 1, 1, 1, 1]
upper_bound = [1500, 1500, 1500, 1500, 1500, 1500]

best_lines = 0
best_branches = 0

for _ in range(1):
    x = random_population(pop_size, n_parameters, lower_bound, upper_bound)
    line, branch = evaluate(x)
    best_lines = max(best_lines, line)
    best_branches = max(best_branches, branch)

end_time = time.time()

print("best lines: ", best_lines)
print("best branches: ", best_branches)
print("Time elapsed: ", end_time - start_time, "seconds")
