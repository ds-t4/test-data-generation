import inspect

import coverage
import numpy as np
from pymoo.core.problem import ElementwiseProblem


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
