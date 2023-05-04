import numpy as np
from pymoo.core.mutation import Mutation


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
