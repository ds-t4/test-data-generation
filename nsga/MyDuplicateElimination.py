from pymoo.core.duplicate import ElementwiseDuplicateElimination


class MyDuplicateElimination(ElementwiseDuplicateElimination):

    def __init__(self, n_cases, n_parameters):
        super().__init__()
        self.n_cases = n_cases
        self.n_parameters = n_parameters

    # eliminate one individual when two individuals share the same valid test inputs

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
