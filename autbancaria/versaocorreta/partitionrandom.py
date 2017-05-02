from random import uniform

from partitiongeneric2 import *


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


def gen_gen_random_pert3():
    topo1 = uniform(0.0,0.3)
    baixo1 = uniform(topo1, 0.5)

    baixo2 = uniform(0.0, 0.3)
    topo2 = uniform(baixo2, 0.75)
    baixo3 = uniform(topo2, 1.0)

    baixo4 = uniform(0.0, 0.5)
    topo3 = uniform(baixo4, 1.0)
    baixo5 = uniform(topo3, 1.0)

    baixo6 = uniform(0.25, 0.75)
    topo4 = uniform(baixo6, 1.0)
    baixo7 = uniform(topo4, 1.0)

    baixo8 = uniform(0.5, 1.0)
    topo5 = uniform(baixo8, 1.0)
    baixo9 = uniform(topo5, 1.0)

    baixo10 = uniform(0.6, 1.0)
    topo6 = uniform(baixo10, 1.0)
    baixo11 = uniform(topo6, 1.0)

    baixo12 = uniform(0.7, 1.0)
    topo7 = uniform(baixo12, 1.0)

    VVL = topo1, baixo1
    VL = baixo2, topo2, baixo3
    L = baixo4, topo3, baixo5
    M = baixo6, topo4, baixo7
    H = baixo8, topo5, baixo9
    VH = baixo10, topo6, baixo11
    VVH = baixo12, topo7

    func_values = (VVL,VL,L,M,H,VH,VVH)

    return gen_gen_pertinence(func_values), func_values


def gen_gen_random_pert4():
    topo1 = uniform(0.0,0.3)
    baixo1 = uniform(topo1, 0.5)

    baixo2 = uniform(0.0, 0.3)
    topo2 = uniform(baixo2, 0.75)
    baixo3 = uniform(topo2, 1.0)

    baixo3_1 = uniform(0.0, 0.3)
    topo2_1 = uniform(baixo3_1, 0.75)
    baixo3_2 = uniform(topo2_1, 1.0)

    baixo4 = uniform(0.0, 0.5)
    topo3 = uniform(baixo4, 1.0)
    baixo5 = uniform(topo3, 1.0)

    baixo6 = uniform(0.25, 0.75)
    topo4 = uniform(baixo6, 1.0)
    baixo7 = uniform(topo4, 1.0)

    baixo8 = uniform(0.5, 1.0)
    topo5 = uniform(baixo8, 1.0)
    baixo9 = uniform(topo5, 1.0)

    baixo9_1 = uniform(0.6, 1.0)
    topo5_1 = uniform(baixo9_1, 1.0)
    baixo9_2 = uniform(topo5_1, 1.0)

    baixo10 = uniform(0.6, 1.0)
    topo6 = uniform(baixo10, 1.0)
    baixo11 = uniform(topo6, 1.0)

    baixo12 = uniform(0.7, 1.0)
    topo7 = uniform(baixo12, 1.0)

    VVVL = topo1, baixo1
    VVL = baixo2, topo2, baixo3
    VL = baixo3_1, topo2_1, baixo3_2
    L = baixo4, topo3, baixo5
    M = baixo6, topo4, baixo7
    H = baixo8, topo5, baixo9
    VH = baixo9_1, topo5_1, baixo9_2
    VVH = baixo10, topo6, baixo11
    VVVH = baixo12, topo7

    func_values = (VVVL,VVL,VL,L,M,H,VH,VVH,VVVH)

    return gen_gen_pertinence(func_values), func_values