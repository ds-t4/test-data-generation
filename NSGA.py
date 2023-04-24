import time

import coverage
import inspect
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem, StarmapParallelization
from pymoo.optimize import minimize
from pymoo.core.sampling import Sampling
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.mutation import Mutation
from pymoo.operators.selection.tournament import TournamentSelection
from pymoo.core.crossover import Crossover
from Util import count_lines

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
        self.tmp = 1
        self.pop_size = 20
        self.f1_score = 0

        super().__init__(n_var=(self.n_parameters + 1) * n_cases, n_obj=3)

    def _evaluate(self, x, out, *args, **kwargs):
        x = x.reshape(self.n_cases, self.n_parameters + 1)

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

        # print(f"Line covered: {lines_covered}, Branches covered: {branches_covered}, #: {f3}")

        out["F"] = np.column_stack([f1, f2, f3])

        # if self.tmp == self.pop_size:
        #     # print('Average:', self.f1_score / self.pop_size)
        #     self.tmp = 1
        #     self.f1_score = 0
        # else:
        #     self.tmp += 1
        #     self.f1_score += f1


def binary_tournament_pareto(pop, P, **kwargs):
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape

    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")

    # the result this function returns
    S = np.full(n_tournaments, -1, dtype=int)

    # now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]

        aF = pop[a].F
        bF = pop[b].F

        S[i] = a
        flag = True
        for j in range(len(aF)):
            if aF[j] > bF[j] and j == 0:
                flag = False
            elif aF[j] < bF[j]:
                flag = True
                break
        if not flag:
            S[i] = b

    return S


def binary_tournament_coverage_focus(pop, P, **kwargs):
    # The P input defines the tournaments and competitors
    n_tournaments, n_competitors = P.shape

    if n_competitors != 2:
        raise Exception("Only pressure=2 allowed for binary tournament!")

    # the result this function returns

    S = np.full(n_tournaments, -1, dtype=int)

    # now do all the tournaments
    for i in range(n_tournaments):
        a, b = P[i]

        aF = pop[a].F
        bF = pop[b].F

        S[i] = b
        for j in range(len(aF)):
            if aF[j] < bF[j]:
                S[i] = a
                break
            elif aF[j] > bF[j]:
                break
    return S


selectionA = TournamentSelection(pressure=2, func_comp=binary_tournament_pareto)
selectionB = TournamentSelection(pressure=2, func_comp=binary_tournament_coverage_focus)


class MySampling(Sampling):

    def _do(self, problem, n_samples, **kwargs):
        X = []
        for _ in range(n_samples):
            individual = []
            for _ in range(problem.n_cases):
                test_inputs = [np.random.randint(problem.lower_bound[i], problem.upper_bound[i]) for i in
                               range(problem.n_parameters)]
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


class MyCrossover(Crossover):
    def __init__(self):
        self.n_parents = 2
        self.n_offsprings = 2
        super().__init__(self.n_parents, self.n_offsprings)

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings(population size), n_var (+1))
        n_parents, n_matings, n_var = X.shape

        X = X.reshape(n_parents, n_matings, problem.n_cases, problem.n_parameters + 1)
        Y = np.full_like(X, None, dtype=object)

        for k in range(n_matings):
            midpoint = np.random.randint(0, problem.n_cases + 1)
            Y[0, k, :] = np.concatenate((X[0, k, :midpoint, :], X[1, k, midpoint:, :]))
            Y[1, k, :] = np.concatenate((X[1, k, :midpoint, :], X[0, k, midpoint:, :]))

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
                if r < 0.15:
                    X[i][j][problem.n_parameters] = (X[i][j][problem.n_parameters] + 1) % 2
                elif r < 0.4:
                    index = np.random.randint(0, problem.n_parameters)
                    X[i][j][index] = np.random.randint(problem.lower_bound[index], problem.upper_bound[index])

        X = X.reshape(len(X), problem.n_var)
        return X


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
    # eliminate_duplicates=MyDuplicateElimination(problem.n_cases, problem.n_parameters))

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
