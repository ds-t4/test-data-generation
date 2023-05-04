import inspect
import time

import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

from sample import bucket_list
from sample import quadratic
from Util import count_lines
from nsga import MyProblem, MySampling, MyCrossover, MyMutation, selectionA

if __name__ == '__main__':
    start_time = time.time()

    problemA = MyProblem(method=bucket_list,
                         n_cases=50,
                         lower_bound=np.full((len(inspect.signature(bucket_list).parameters),), 1),
                         upper_bound=np.full((len(inspect.signature(bucket_list).parameters),), 1500))

    problemB = MyProblem(method=quadratic,
                         n_cases=50,
                         lower_bound=np.full((len(inspect.signature(quadratic).parameters),), 1),
                         upper_bound=np.full((len(inspect.signature(quadratic).parameters),), 2000))

    algorithm = NSGA2(pop_size=50,
                      sampling=MySampling(),
                      crossover=MyCrossover(),
                      mutation=MyMutation(),
                      selection=selectionA,
                      eliminate_duplicates=False)
    # eliminate_duplicates=MyDuplicateElimination(problemA.n_cases, problemA.n_parameters))

    res = minimize(problemA,
                   algorithm,
                   ("n_gen", 50),
                   verbose=False)

    X = res.X
    end_time = time.time()

    total_lines = count_lines(inspect.getfile(bucket_list))
    print(f'Function values: {res.F}')
    print(f'Design variables: {res.X}')
    print(f'Line coverage: {- res.F[0, 0] * 100 / total_lines} %, total {total_lines}')
    print(f'Time elapsed: {end_time - start_time} seconds')
