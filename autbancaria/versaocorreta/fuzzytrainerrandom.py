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


    ######################## Criar regras basicas ###########################

    def calcRegras(entradas, saidas):
        regras = []
        for entrada, saida in zip(entradas, saidas):
            termos = []

            for i in range(len(entrada)):
                pertinencias = []

                for pertf in PERT_FUNCTIONS[i]:
                    pert = pertf(entrada[i])
                    pertinencias.append(pert)

                maior = max(pertinencias)
                index_maior = pertinencias.index(maior)
                lingValue = LING_VALUES[index_maior]
                termos.append((lingValue, maior))

            termos.append(CLASSES[int(saida)])
            regras.append(termos)

        return regras


    def printRegras(regras):
        for r in regras:
            print("Se", end=" ")
            for i in range(len(INPUT_VARS)):
                print(INPUT_VARS[i], "=", r[i], end=" ")
                if i != len(INPUT_VARS) - 1: print("e", end=" ")
            print("entao", r[4])


    regras = calcRegras(ENTRADAS, SAIDAS)
    printRegras(regras)


    ###################### Calcular niveis de disparo ########################



    def calcula_niveis_disparo(norma_t):
        niveis_disparos = []
        for r in regras:
            nivel = norma_t([t[1] for t in r[:4]])
            niveis_disparos.append(nivel)
        return niveis_disparos

    def produtorio(list):
        res = 1
        for item in list:
            res *= item
        return res

    niveis_disparos = calcula_niveis_disparo(produtorio) #norma-t = min
    # niveis_disparos = calcula_niveis_disparo(produtorio) #norma-t = produtorio
    print(niveis_disparos)

    ###################### encontrar antecedentes iguais #################

    antecedentes = {}

    for i in range(len(regras)):
        ante = tuple([regras[i][v][0] for v in range(len(INPUT_VARS))])
        if ante not in antecedentes.keys():
            antecedentes[ante] = [i]
        else:
            antecedentes[ante].append(i)

    print(antecedentes)

    ##################### filtrar regras pelo antecedente com maior regra de disparo ################

    regras_finais = []
    for ante, indices in antecedentes.items():
        max_nivel_disparo = max([niveis_disparos[i] for i in indices])
        indice_max = niveis_disparos.index(max_nivel_disparo)

        regra = regras[indice_max]
        regras_finais.append(regra)

    printRegras(regras_finais)
    print(len(regras))
    print(len(regras_finais))

    ## testando: ####

    from inferencia import *
    acertos = matchRegras(ENTRADASTEST, SAIDASTEST, regras_finais, \
                      PERT_FUNCTIONS, LING_VALUES, CLASSES) * 100

    results.append((acertos, FUNC_VALUES))

print([r[0] for r in results])


print(max(results)[0], "% de acertos.")
