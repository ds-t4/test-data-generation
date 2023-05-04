import numpy as np
from pymoo.core.sampling import Sampling


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
