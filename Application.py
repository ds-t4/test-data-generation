import streamlit as st
import numpy as np

from BucketList import bucket_list
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from NSGA import MyProblem, MyCrossover, MyMutation, MySampling, binary_tournament, TournamentSelection
import inspect

st.title('Test cases generation')


with st.form(key='background'):
    n_cases = st.text_input('Number of cases')
    option = st.selectbox('Generation tendency',
                          ('Coverage', 'Number of Cases'))
    run_button = st.form_submit_button(label='Submit')

if run_button:
    problem = MyProblem(method=bucket_list,
                        n_cases=10,
                        lower_bound=np.full(
                            (len(inspect.signature(bucket_list).parameters),), 1),
                        upper_bound=np.full((len(inspect.signature(bucket_list).parameters),), 1500))

    algorithm = NSGA2(pop_size=10,
                      sampling=MySampling(),
                      crossover=MyCrossover(),
                      mutation=MyMutation(),
                      selection=TournamentSelection(
                          pressure=2, func_comp=binary_tournament),
                      eliminate_duplicates=False)
    # eliminate_duplicates=MyDuplicateElimination(problem.n_cases, problem.n_parameters))

    res = minimize(problem,
                   algorithm,
                   ("n_gen", 20),
                   verbose=False,
                   seed=1)

    X = res.X

    st.write(f"Function values: {res.F}")
    st.write(f"Design variables: {res.X}")

# uploaded_file = st.file_uploader("Choose a python file")
# if uploaded_file is not None:
#     print(uploaded_file)
