
def calcula_disparo_min(regra):
    return min([t[1] for t in regra[:4]])

def calcula_disparo_prod(regra):
    def produtorio(list):
        res = 1
        for item in list:
            res *= item
        return res

    return produtorio([t[1] for t in regra[:4]])

def calcula_centroid(maiores, pert_saida):
    q = 100
    parte_cima = 0
    parte_baixo = 0
    for k in range(1, q):
        x = k / q
        perts = []
        for k in range(len(pert_saida)):
            perts.append(pert_saida[k](x, limite=maiores[k]))
        pert = max(perts)
        parte_cima += x * pert
        parte_baixo += pert

    x = parte_cima / parte_baixo if parte_baixo != 0 else 0
    perts = []
    for k in range(len(pert_saida)):
        perts.append(pert_saida[k](x, limite=maiores[k]))
    pert = max(perts)

    return perts.index(pert)


def max_args(maiores,pert_funcion):
    return maiores.index(max(maiores))

def inferencia(entrada, regras, pert_functions, pert_saida, ling_values, classes, defuzzy=calcula_centroid, norma_t=calcula_disparo_min):
    vars = [[] for _ in range(len(entrada))]


    # Calcula pertinência das variáveis:
    for i in range(len(entrada)):
        pertinencias = []

        for pertf in pert_functions[i]:
            pert = pertf(entrada[i])
            pertinencias.append(pert)

        # Retira pertinências iguais a zero e insere em vars
        for p in range(len(pertinencias)):
            pert = pertinencias[p]
            if pert != 0:
                vars[i].append([ling_values[p], pert])

    import itertools
    #cria combinacoes das vars, formando antecedentes de regras
    combinacoes = [list(c) for c in list(itertools.product(*vars))]

    #estrai apenas os termos linguísticos das combinacoes
    comb_limpas = [[r[0][0], r[1][0], r[2][0], r[3][0]] \
                   for r in combinacoes]

    antecedentes_regras = [regra[0:4] for regra in regras]

    to_remove = []
    for c, cl in zip(combinacoes, comb_limpas):
        if cl not in antecedentes_regras:
            to_remove.append(c)
        else:
            c.append(regras[antecedentes_regras.index(cl)][4])

    # Remove combinacoes que não estão nas regras
    combinacoes = [c for c in combinacoes if c not in to_remove]

    niveis_disparo = []
    for comb in combinacoes:
        nivel_disparo = norma_t(comb)
        niveis_disparo.append(nivel_disparo)

    maiores = [0.,0.,0.]
    regras = [-1,-1,-1]
    niveis = [-1,-1,-1]
    for i in range(len(combinacoes)):
        comb = combinacoes[i]
        nivel = niveis_disparo[i]
        for k in range(len(classes)):
            if comb[4] == classes[k] and nivel > maiores[k]:
                maiores[k] = nivel
                regras[k] = comb
                niveis[k] = nivel

    saida = defuzzy(maiores, pert_saida)

    return classes[saida], regras, niveis

def matchRegras(entradas, saidas, regras, pert_functions, ling_values, classes, defuzzy=calcula_centroid, norma_t=calcula_disparo_min):
    acertos = 0
    for entrada, saida in zip(entradas, saidas):

        if inferencia(entrada, regras, pert_functions, ling_values, classes, defuzzy, norma_t) == saida:
            acertos += 1

    return acertos / len(entradas)
