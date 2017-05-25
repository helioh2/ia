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

from partitionrandom import *

results = []

for _ in range(1000):

    PERT_FUNCTIONS_GENS, FUNC_VALUES = gen_gen_random_pert2()

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

    from criarregras import *

    calcregras = CalcRegras(ENTRADAS, SAIDAS, PERT_FUNCTIONS, LING_VALUES, CLASSES, INPUT_VARS, norma_t=min)
    regras_finais = calcregras.calcula_regras_finais()

    ## testando: ####

    from inferencia import *
    acertos = matchRegras(ENTRADASTEST, SAIDASTEST, regras_finais, \
                      PERT_FUNCTIONS, LING_VALUES, CLASSES) * 100

    results.append((acertos, FUNC_VALUES))


print([r[1] for r in results])

print(max(results)[0], "% de acertos.")
print("Particionamento utilizado:",max(results)[1])
