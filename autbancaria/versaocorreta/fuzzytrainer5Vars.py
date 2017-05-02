################## PREPARACAO ##################



def lerArquivo(filename):
    f = open(filename, "r")

    entradas = []
    saidas = []

    for line in f:
        values = line.split(",")
        entradas.append([float(v) for v in values[:4]])
        saidas.append(float(values[4].rstrip()))

    f.close()

    print(entradas)
    print(saidas)

    return (entradas, saidas)


FILENAMETRAIN = "dadostrain.txt"
ENTRADAS, SAIDAS = lerArquivo(FILENAMETRAIN)

FILENAMETEST = "dadostest.txt"
ENTRADASTEST, SAIDASTEST = lerArquivo(FILENAMETEST)

CLASSES = ["autentica", "falsificada"]
INPUT_VARS = ["variance", "skewness", "curtosis", "entropy"]
LING_VALUES = ["very low", "low", "medium", "high", "very high"]

MAXVARS = []
MINVARS = []


def calculaMaxEMins():
    for i in range(len(INPUT_VARS)):
        varss = [entrada[i] for entrada in ENTRADAS + ENTRADASTEST]
        maxvar = max(varss)
        minvar = min(varss)
        MAXVARS.append(maxvar)
        MINVARS.append(minvar)

    print(MAXVARS)
    print(MINVARS)


calculaMaxEMins()


################# funcoes de pertinencia (grid uniforme) #################

from partitiongeneric2 import *

VL = (0.1, 0.3)
L = (0.1, 0.3, 0.5)
M = (0.3, 0.5, 0.7)
H = (0.5, 0.7, 0.9)
VH = (0.7, 0.9)

FUNC_VALUES = (VL,L,M,H,VH)

PERT_FUNCTIONS_GENS = gen_gen_pertinence(FUNC_VALUES)

PERT_FUNCTIONS = []

def generate_pertinence_functions(pertFunctionsGens):
    pertFunctions = []
    for v in range(len(INPUT_VARS)):
        var_functions = []
        for k in range(len(LING_VALUES)):
            gen = pertFunctionsGens[k]
            func = gen(MINVARS[v], MAXVARS[v])
            var_functions.append(func)
        pertFunctions.append(var_functions)
    return pertFunctions


PERT_FUNCTIONS = generate_pertinence_functions(PERT_FUNCTIONS_GENS)

print(PERT_FUNCTIONS)


######################## Criar regras ###########################

from criarregras import CalcRegras

calcregras = CalcRegras(ENTRADAS, SAIDAS, PERT_FUNCTIONS, LING_VALUES, CLASSES, INPUT_VARS)
regras_finais = calcregras.calcula_regras_finais()

## testando: ####

from inferencia import *

print("----------")
print(matchRegras(ENTRADASTEST, SAIDASTEST, regras_finais, \
                  PERT_FUNCTIONS, LING_VALUES, CLASSES, norma_t=calcula_disparo_min) * 100, "% de acertos.")
print("----------")
