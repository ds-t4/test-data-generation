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

if 'best_cases_filtered' not in st.session_state:
    st.session_state['best_cases_filtered'] = []

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
    end_time = time.time()

    X = res.X

    total_lines = count_lines(inspect.getfile(p))
    max_cov, index, max_index = 0, 0, 0
    for (cov, _, _) in res.F:
        if -cov > max_cov:
            max_cov = -cov
            max_index = index
        index += 1
    best_cases = res.X[max_index]
    n_args = len(inspect.signature(p).parameters)
    best_cases = np.array(best_cases).reshape(len(best_cases) // (n_args+1), n_args+1)
    best_cases_filtered = []
    for case in best_cases:
        if case[-1]:
            best_cases_filtered.append(list(case[:-1]))
    st.session_state['best_cases_filtered'] = best_cases_filtered
    st.write(f'Best test cases: {res.F}')
    st.write(f'Best test cases: {best_cases_filtered}')
    st.write(f'Line coverage: {- res.F[0, 0] * 100 / total_lines} %')
    st.write(f'Time elapsed: {end_time - start_time} seconds')

if st.button('Save the data as CSV'):
    best_cases = np.array(st.session_state['best_cases_filtered'])
    np.savetxt('best_cases.csv', best_cases, fmt='%.6f', delimiter=',')
    st.write('Saved!')
