import inspect
import time

import numpy as np
import streamlit as st
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

from BucketList import bucket_list
from Calculator import quadratic
from NSGA import MyProblem, MyCrossover, MyMutation, MySampling, count_lines, selectionA, selectionB

st.set_page_config(page_title="Test Generation", page_icon=":sunglasses:")
st.title('Test Cases Generation')
st.write("DSSE T4")

with st.form(key='background'):
    problem = st.radio('Problem', ('Bucket List', 'Quadratic Equation'))
    target_cases = st.number_input('Target number of test cases', min_value=1, max_value=100, value=30, step=1)
    tendency = st.radio('Metrics tendency', ('Coverage Focused', 'Balanced'))
    lower_bound = st.number_input('Lower bound', min_value=-100000, max_value=100000, value=1, step=1)
    upper_bound = st.number_input('Upper bound', min_value=-100000, max_value=100000, value=2000, step=1)
    population_size = st.number_input('Population size', min_value=1, max_value=100, value=50, step=1)
    n_generation = st.number_input('Number of generations', min_value=1, max_value=100, value=50, step=1)
    run_button = st.form_submit_button(label='RUN')

if run_button:
    if problem == 'Bucket List':
        p = bucket_list
    else:
        p = quadratic
    target_cases = int(target_cases * 1.75)
    lower_bound = int(lower_bound)
    upper_bound = int(upper_bound)
    population_size = int(population_size)
    n_generation = int(n_generation)
    if tendency == 'Coverage Focused':
        selection = selectionB
    else:
        selection = selectionA

    problem_chosen = MyProblem(method=p,
                               n_cases=target_cases,
                               lower_bound=np.full((len(inspect.signature(bucket_list).parameters),), lower_bound),
                               upper_bound=np.full((len(inspect.signature(bucket_list).parameters),), upper_bound))

    algorithm = NSGA2(pop_size=population_size,
                      sampling=MySampling(),
                      crossover=MyCrossover(),
                      mutation=MyMutation(),
                      selection=selection,
                      eliminate_duplicates=False)

    start_time = time.time()
    res = minimize(problem_chosen,
                   algorithm,
                   ("n_gen", n_generation),
                   verbose=False,
                   seed=1)

    X = res.X
    end_time = time.time()

    total_lines = count_lines(inspect.getfile(bucket_list))
    st.write(f'Function values: {res.F}')
    st.write(f'Design variables: {res.X}')
    st.write(f'Line coverage: {- res.F[0, 0] * 100 / total_lines} %')
    st.write(f'Time elapsed: {end_time - start_time} seconds')
