import numpy as np
from pymoo.operators.selection.tournament import TournamentSelection


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
