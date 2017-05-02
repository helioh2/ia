def lerArquivo(filename):
    f = open(filename, "r")

    entradas = []
    saidas = []

    for line in f:
        values = line.split(",")
        entradas.append([float(v) for v in values[:4]])
        saidas.append(float(values[4].rstrip()))

    f.close()

    # print(entradas)
    # print(saidas)

    return (entradas, saidas)


FILENAMETRAIN = "dadostrain.txt"
ENTRADAS, SAIDAS = lerArquivo(FILENAMETRAIN)

FILENAMETEST = "dadostest.txt"
ENTRADASTEST, SAIDASTEST = lerArquivo(FILENAMETEST)

ENTRADASTOTAL = ENTRADAS + ENTRADASTEST
SAIDASTOTAL = SAIDAS + SAIDASTEST

entradasdict = {}
inconsistentes = []

for i in range(len(ENTRADASTOTAL)):
    entrada = tuple(ENTRADASTOTAL[i])
    if entrada not in entradasdict.keys():
        entradasdict[entrada] = [i]
    else:
        for j in entradasdict[entrada]:
            if SAIDASTOTAL[j] != SAIDASTOTAL[i]:
                inconsistentes.append(i)
                break
        entradasdict[entrada].append(i)

print(inconsistentes)

