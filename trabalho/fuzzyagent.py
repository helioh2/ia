################## PREPARACAO ##################

NOME_SAIDA = "decisao"
CLASSES = ["aceita", "replica", "rejeita"]
INPUT_VARS = ["credibilidade", "importancia_objetivo", "alcancabilidade_objetivo", "esforco_tarefa"]
LING_VALUES = ["baixo", "medio", "alto"]

MINVARS = [0,0,0,0]
MAXVARS = [1,1,1,1]

################# funcoes de pertinencia (grid uniforme) #################

from partitiongeneric2 import *

L = (0.2, 0.4)
M = (0.3, 0.5, 0.7)
H = (0.6, 0.8)

FUNC_VALUES = (L, M, H)

PERT_FUNCTIONS_GENS = gen_gen_pertinence(FUNC_VALUES)

def generate_pertinence_functions(pert_functions_gens):
    pert_functions = []
    for v in range(len(INPUT_VARS)):
        var_functions = []
        for k in range(len(LING_VALUES)):
            gen = pert_functions_gens[k]
            func = gen(MINVARS[v], MAXVARS[v])
            var_functions.append(func)
        pert_functions.append(var_functions)
    return pert_functions


PERT_FUNCTIONS = generate_pertinence_functions(PERT_FUNCTIONS_GENS)

L = (0.2, 0.4)
M = (0.3, 0.5, 0.7)
H = (0.6, 0.8)

FUNC_VALUES_SAIDA = (L, M, H)

PERT_FUNCTIONS_GENS_SAIDA = gen_gen_pertinence(FUNC_VALUES_SAIDA)

PERT_SAIDA = []
for k in range(len(CLASSES)):
    gen = PERT_FUNCTIONS_GENS_SAIDA[k]
    func = gen(0, 1)
    PERT_SAIDA.append(func)

######################## Criar regras ###########################
##Criar proprias
regras = []
import itertools
regras_sem_cons = list(itertools.product(LING_VALUES, repeat=4))
# print(regras_sem_cons)
for lin in range (len(regras_sem_cons)):
    print(regras_sem_cons[lin])


with open("regras1.csv", "r") as f:
    mylist = f.read().splitlines()
    for line in mylist:
        regras.append(line.split(","))


def printRegras(regras):
    for r in regras:
        print("Se", end=" ")
        for i in range(len(INPUT_VARS)):
            print(INPUT_VARS[i], "=", r[i], end=" ")
            if i != len(INPUT_VARS) - 1: print("e", end=" ")
        print("entao", r[4])

printRegras(regras)

## testando: ####

from inferencia import *
from random import random


print("#### Teste com entradas personalizadas:")

ENTRADASTEST = [
            [0.9,0.9,0.9,0.1],
            [0.6,0.6,0.6,0.6],
            [0.2,0.2,0.2,0.9]

]

print("----------")
for entrada in ENTRADASTEST:
    saida = inferencia(entrada, regras, \
                  PERT_FUNCTIONS, PERT_SAIDA, LING_VALUES, CLASSES, norma_t=calcula_disparo_min)[0]
    print("Entradas: ",entrada)
    print(saida)
print("----------")



print("#### Teste com entradas aleatórias:")

ENTRADASTEST = []
for k in range(50):
    ENTRADASTEST.append([random(),random(), random(), random()])

print("----------")
for entrada in ENTRADASTEST:
    saida = inferencia(entrada, regras, \
                  PERT_FUNCTIONS, PERT_SAIDA, LING_VALUES, CLASSES,
                    defuzzy=calcula_centroid, norma_t=calcula_disparo_min)
    print("Entradas: ",entrada)
    print(saida[0])
print("----------")


print("#### Teste com entradas dos cenários")

ENTRADASTEST = []
ENTRADASTEST.append([0.5, 0.9, 0.3, 0.6])
ENTRADASTEST.append([0.5, 0.6, 0.8, 0.6])

print("----------")
for entrada in ENTRADASTEST:
    saida,regrasdisp,niveis = inferencia(entrada, regras, \
                  PERT_FUNCTIONS, PERT_SAIDA, LING_VALUES, CLASSES, defuzzy=calcula_centroid, norma_t=calcula_disparo_min)
    print("Entradas: ",entrada)
    print(saida)
    print(regrasdisp)
    print(niveis)
print("----------")




