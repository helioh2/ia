from random import uniform

from autbancaria2.versaoantiga.partitiongeneric2 import *


def gen_gen_random_pert():
    topo1 = uniform(0.0,0.3)
    baixo1 = uniform(topo1, 0.5)

    baixo2 = uniform(0.0, 0.3)
    topo2 = uniform(baixo2, 1.0)
    baixo3 = uniform(topo2, 1.0)

    baixo4 = uniform(0.0, 1.0)
    topo3 = uniform(baixo4, 1.0)
    baixo5 = uniform(topo3, 1.0)

    baixo6 = uniform(0.3, 1.0)
    topo4 = uniform(baixo6, 1.0)
    baixo7 = uniform(topo4, 1.0)

    baixo8 = uniform(0.5, 1.0)
    topo5 = uniform(baixo8, 1.0)

    VL = topo1, baixo1
    L = baixo2, topo2, baixo3
    M = baixo4, topo3, baixo5
    H = baixo6, topo4, baixo7
    VH = baixo8, topo5

    func_values = (VL,L,M,H,VH)

    return gen_gen_pertinence(func_values), func_values


def gen_gen_random_pert2():
    topo1 = uniform(0.0,0.3)
    baixo1 = uniform(topo1, 0.75)

    baixo2 = uniform(0.0, 0.5)
    topo2 = uniform(baixo2, 1.0)
    baixo3 = uniform(topo2, 1.0)

    baixo4 = uniform(0.0, 1.0)
    topo3 = uniform(baixo4, 1.0)
    baixo5 = uniform(topo3, 1.0)

    baixo6 = uniform(0.25, 1.0)
    topo4 = uniform(baixo6, 1.0)
    baixo7 = uniform(topo4, 1.0)

    baixo8 = uniform(0.25, 1.0)
    topo5 = uniform(baixo8, 1.0)

    VL = topo1, baixo1
    L = baixo2, topo2, baixo3
    M = baixo4, topo3, baixo5
    H = baixo6, topo4, baixo7
    VH = baixo8, topo5

    func_values = (VL,L,M,H,VH)

    return gen_gen_pertinence(func_values), func_values