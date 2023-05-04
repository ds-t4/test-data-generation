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

        X = X.reshape(n_parents, n_matings, problem.n_cases, problem.n_parameters + 1)
        Y = np.full_like(X, None, dtype=object)

        for k in range(n_matings):
            midpoint = np.random.randint(0, problem.n_cases + 1)
            Y[0, k, :] = np.concatenate((X[0, k, :midpoint, :], X[1, k, midpoint:, :]))
            Y[1, k, :] = np.concatenate((X[1, k, :midpoint, :], X[0, k, midpoint:, :]))

        Y = Y.reshape(self.n_offsprings, n_matings, n_var)
        return Y
