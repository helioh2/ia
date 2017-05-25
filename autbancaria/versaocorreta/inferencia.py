
def pertinence_saida_autentica(x, limite=1):
    if x < 0.3:
        return limite
    elif 0.3 <= x < 0.7:
        pert = 1 - (x - 0.3) / 0.4
        return pert if pert < limite else limite
    else:
        return 0


def pertinence_saida_falsa(x, limite=1):
    if x > 0.7:
        return limite
    elif 0.3 < x <= 0.7:
        pert = (x - 0.3) / 0.4
        return pert if pert < limite else limite
    else:
        return 0


def calcula_disparo_min(regra):
    return min([t[1] for t in regra[:4]])

def calcula_disparo_prod(regra):
    def produtorio(list):
        res = 1
        for item in list:
            res *= item
        return res

    return produtorio([t[1] for t in regra[:4]])

def calcula_centroid(maior_0, maior_1):
    q = 100
    parte_cima = 0
    parte_baixo = 0
    for k in range(1, q):
        x = k / q
        pert0 = pertinence_saida_autentica(x, limite=maior_0)
        pert1 = pertinence_saida_falsa(x, limite=maior_1)
        pert = max([pert0, pert1])
        parte_cima += x * pert
        parte_baixo += pert

    x = parte_cima / parte_baixo if parte_baixo != 0 else 0
    pert0 = pertinence_saida_autentica(x, limite=maior_0)
    pert1 = pertinence_saida_falsa(x, limite=maior_1)
    pert = max([pert0, pert1])

    if pert == pert0:
        return 0.0
    elif pert == pert1:
        return 1.0

def defuzzy_max(maior_0, maior_1):
    return 0.0 if maior_0 > maior_1 else 1.0




def inferencia(entrada, regras, pert_functions, ling_values, classes, defuzzy=calcula_centroid, norma_t=calcula_disparo_min):
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

    #extrai apenas os termos linguísticos das regras
    regras_limpas = [[r[0][0], r[1][0], r[2][0], r[3][0]] \
                     for r in regras]
    #estrai apenas os termos linguísticos das combinacoes
    comb_limpas = [[r[0][0], r[1][0], r[2][0], r[3][0]] \
                   for r in combinacoes]


    to_remove = []
    for c, cl in zip(combinacoes, comb_limpas):
        if cl not in regras_limpas:
            to_remove.append(c)
        else:
            c.append(regras[regras_limpas.index(cl)][4])

    # Remove combinacoes que não estão nas regras
    combinacoes = [c for c in combinacoes if c not in to_remove]

    niveis_disparo = []
    for comb in combinacoes:
        nivel_disparo = norma_t(comb)
        niveis_disparo.append(nivel_disparo)

    maior_0 = 0.
    maior_1 = 0.
    for i in range(len(combinacoes)):
        comb = combinacoes[i]
        nivel = niveis_disparo[i]
        if comb[4] == classes[0] and nivel > maior_0:
            maior_0 = nivel
        elif comb[4] == classes[1] and nivel > maior_1:
            maior_1 = nivel

    saida = defuzzy(maior_0, maior_1)

    return saida

def matchRegras(entradas, saidas, regras, pert_functions, ling_values, classes, defuzzy=calcula_centroid, norma_t=calcula_disparo_min):
    acertos = 0
    for entrada, saida in zip(entradas, saidas):

        if inferencia(entrada, regras, pert_functions, ling_values, classes, defuzzy, norma_t) == saida:
            acertos += 1

    return acertos / len(entradas)
