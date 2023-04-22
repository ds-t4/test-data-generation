import coverage
import inspect
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.core.sampling import Sampling
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.mutation import Mutation

from BucketList import bucket_list
from Calculator import quadratic


class MyProblem(ElementwiseProblem):

    def __init__(self, method, n_cases, lower_bound, upper_bound):
        self.method = method
        self.n_parameters = len(inspect.signature(method).parameters)
        self.n_cases = n_cases
        self.method = method
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        super().__init__(n_var=(self.n_parameters + 1) * n_cases, n_obj=3)

    def _evaluate(self, x, out, *args, **kwargs):
        x = x.reshape(self. n_cases, self.n_parameters + 1)

        cov = coverage.Coverage(branch=True)
        cov.start()

        for i in range(len(x)):
            if x[i, self.n_parameters] == 1:
                parameters = [x[i, j] for j in range(self.n_parameters)]
                self.method(*parameters)

        cov.stop()
        data = cov.get_data()

        lines_covered = sum(len(data.lines(filename)) for filename in data.measured_files())
        branches_covered = sum(len(data.arcs(filename)) for filename in data.measured_files())

        f1 = -lines_covered
        f2 = -branches_covered
        f3 = np.sum(x[:, self.n_parameters])

        print(f"Line covered: {lines_covered}, Branches covered: {branches_covered}, #: {f3}")

        out["F"] = np.column_stack([f1, f2, f3])


class MySampling(Sampling):

    def _do(self, problem, n_samples, **kwargs):
        X = []
        for _ in range(n_samples):
            individual = []
            for _ in range(problem.n_cases):
                test_inputs = [np.random.randint(problem.lower_bound[i], problem.upper_bound[i]) for i in range(problem.n_parameters)]
                test_inputs.append(1)
                individual.append(test_inputs)
            X.append(individual)

        result = np.array(X).reshape(n_samples, problem.n_var)
        return result


class MyDuplicateElimination(ElementwiseDuplicateElimination):

    def __init__(self, n_cases, n_parameters):
        super().__init__()
        self.n_cases = n_cases
        self.n_parameters = n_parameters


    def is_equal(self, a, b):
        a_reshape = a.X.reshape(self.n_cases, self.n_parameters + 1)
        b_reshape = b.X.reshape(self.n_cases, self.n_parameters + 1)
        a_reshape_filter = set()
        b_reshape_filter = set()
        for test_case in a_reshape:
            if test_case[-1] == 1:
                a_reshape_filter.add(str(test_case[:-1]))
        for test_case in b_reshape:
            if test_case[-1] == 1:
                b_reshape_filter.add(str(test_case[:-1]))
        if a_reshape_filter == b_reshape_filter:
            return True
        return False

import random
import numpy as np
from pymoo.core.crossover import Crossover

class MyCrossover(Crossover):
    def __init__(self):
        self.n_parents = 2
        self.n_offsprings = 2
        super().__init__(self.n_parents, self.n_offsprings)

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings(population size), n_var (+1))
        n_parents, n_matings, n_var = X.shape

        X = X.reshape(n_parents, n_matings, problem.n_cases, problem.n_parameters+1)
        Y = np.full_like(X, None, dtype=object)
        for k in range(n_matings):
            # get the first and the second parent
            # a, b = X[0, k, :], X[1, k, :]

            midpoint = np.random.randint(0, n_var)
            a = X[0, k, :midpoint, :]
            Y[0,k,:] = np.concatenate((X[0, k, :midpoint,:], X[1, k, midpoint:,:]))
            Y[1,k,:] = np.concatenate((X[1, k, :midpoint,:], X[0, k, midpoint:,:]))

        Y = Y.reshape(self.n_offsprings, n_matings, n_var)
        return Y


class MyMutation(Mutation):
    def __init__(self):
        super().__init__()

    def _do(self, problem, X, **kwargs):
        X = X.reshape(len(X), problem.n_cases, problem.n_parameters + 1)
        for i in range(len(X)):
            for j in range(problem.n_cases):
                r = np.random.random()
                if r < 0.3:
                    X[i][j][problem.n_parameters] = 1 - X[i][j][problem.n_parameters]
                elif r < 0.8:
                    index = np.random.randint(0, problem.n_parameters)
                    X[i][j][index] = np.random.randint(problem.lower_bound[index], problem.upper_bound[index])

        X = X.reshape(len(X), problem.n_var)
        return X


problem = MyProblem(method=bucket_list,
                    n_cases=20,
                    lower_bound= np.full((6,), 1),
                    upper_bound = np.full((6,), 1500))

algorithm = NSGA2(pop_size=20,
                  sampling=MySampling(),
                  crossover=MyCrossover(),
                  mutation=MyMutation(),
                  eliminate_duplicates=MyDuplicateElimination(problem.n_cases, problem.n_parameters))

res = minimize(problem,
               algorithm,
               ("n_gen", 50),
               verbose=False,
               seed=1)

X = res.X

# print the results
print(f"Function values: {res.F}")
print(f"Design variables: {res.X}")
print(f"Design variables: {res.X[0]}")

