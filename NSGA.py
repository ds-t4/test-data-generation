import coverage
import numpy as np

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

from Calculator import *
from pymoo.core.variable import Real, Integer, Choice, Binary
from pymoo.core.mixed import MixedVariableGA

from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival

class MyProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        vars = {"x": Integer(bounds=(0, 10))}
        super().__init__(vars=vars, n_obj=2, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
        cov = coverage.Coverage(branch=True)

        cov.start()
        x = X["x"]
        print("x is ", x)
        is_prime(x)
        # .. call your code ..
        cov.stop()
        data = cov.get_data()


        lines_total = sum(len(data.lines(filename)) for filename in data.measured_files())
        # print(lines_total)
        lines_covered = sum(1 for filename in data.measured_files() if any(data.lines(filename)))
        line_coverage = 100.0 * lines_covered / lines_total
        print("Line coverage: {:.2f}%".format(line_coverage))

        # Calculate branch coverage
        branches_total = sum(len(data.arcs(filename)) for filename in data.measured_files())
        branches_covered = sum(1 for filename in data.measured_files() if any(data.arcs(filename)))
        if branches_total == 0:
            branch_coverage = 0.0
        else:
            branch_coverage = 100.0 * branches_covered / branches_total
        print("Branch coverage: {:.2f}%".format(branch_coverage))

        cov.save()

        f1 = line_coverage * -1
        f2 = branch_coverage * -1
        out["F"] = [f1, f2]

problem = MyProblem()

algorithm = MixedVariableGA(pop_size=20, survival=RankAndCrowdingSurvival())

res = minimize(problem,
               algorithm,
               ("n_gen", 100),
               verbose=False,
               seed=1)
X = res.X

# print the results
print(f"Function values: {res.F}")
print(f"Design variables: {res.X}")