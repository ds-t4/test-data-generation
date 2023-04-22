# -*- coding: utf-8 -*-
"""T4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YwnH6Qe3kbC6qtYv_IC_c9B6Af6V6ljv
"""


import coverage
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.optimize import minimize

from Calculator import quadratic


class MyProblem(ElementwiseProblem):

    def __init__(self, n_parameters, n_var, lower_bound, upper_bound):
        self.n_parameters = n_parameters
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        super().__init__(n_var=n_var, n_obj=2)

    def _evaluate(self, x, out, *args, **kwargs):
        print('evaluating', x)

        cov = coverage.Coverage(branch=True)

        cov.start()

        for i in range(len(x)):
            if x[i, self.n_parameters] == 1:
                quadratic(x[i, 0], x[i, 1], x[i, 2], x[i, 3], x[i, 4])

        cov.stop()
        data = cov.get_data()

        print(data.measured_files())

        lines_covered = sum(len(data.lines(filename)) for filename in data.measured_files())
        print(f"Line covered: {lines_covered}")

        branches_covered = sum(len(data.arcs(filename)) for filename in data.measured_files())
        print(f"Branches coverage: {branches_covered}")

        f1 = -lines_covered
        f2 = -branches_covered

        out["F"] = np.column_stack([f1, f2])

from pymoo.core.sampling import Sampling

class MySampling(Sampling):

    def _do(self, problem, n_samples, **kwargs):
        X = []
        for _ in range(n_samples):
            individual = []
            for _ in range(problem.n_var):
                test_inputs = [np.random.randint(problem.lower_bound[i], problem.upper_bound[i]) for i in range(problem.n_parameters)]
                test_inputs.append(1)
                individual.append(test_inputs)
            X.append(individual)
        print(np.array(X))

        return np.array(X)

from pymoo.core.duplicate import ElementwiseDuplicateElimination

class MyDuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        # for i,j in zip(a.X, b.X):
        #     if i != j:
        #         return False
        return False

import random
import numpy as np
from pymoo.core.crossover import Crossover

class MyCrossover(Crossover):
    def __init__(self):
        super().__init__(2, 2)

    def _do(self, problem, X, **kwargs):
        print('crossiver', X)
        print('crossiver', X.shape)
        # The input of has the following shape (n_parents, n_matings(population size), n_var (+1))
        _, n_matings, n_var, n_param = X.shape
        Y = np.full_like(X, None, dtype=object)
        print(Y.shape)
        for k in range(n_matings):
            # get the first and the second parent
            # a, b = X[0, k, :], X[1, k, :]

            midpoint = np.random.randint(0, n_var)
            a = X[0, k, :midpoint, :]
            print("a.shape is ", a.shape)
            Y[0,k,:] = np.concatenate((X[0, k, :midpoint,:], X[1, k, midpoint:,:]))
            print(Y[0,k,:].shape)
            Y[1,k,:] = np.concatenate((X[1, k, :midpoint,:], X[0, k, midpoint:,:]))

        return Y

from pymoo.core.mutation import Mutation

class MyMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):
        print('mutation', X)
        for i in range(len(X)):
            r = np.random.random()
            if r < 0.3:
                X[i][problem.n_parammeters] = 1 - X[i][problem.n_parammeters]
            elif r < 0.8:
                index = np.random.randint(0, problem.n_parammeters)
                X[i][index] = np.random.randint(problem.lower_bound[index], problem.upper_bound[index])
        return X

problem = MyProblem(5, 3, [-10, -10, -10, -10, -10], [10, 10, 10, 10, 10])

algorithm = NSGA2(pop_size=10,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination())

res = minimize(problem,
               algorithm,
               ("n_gen", 10),
               verbose=False,
               seed=1)
X = res.X

# print the results
print(f"Function values: {res.F}")
print(f"Design variables: {res.X}")
