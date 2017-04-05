
FILENAME = "dados_autent_bancaria.txt"

def lerArquivo():
    f = open(FILENAME,"r")
    
    entradas = []
    saidas = []
    
    for line in f:
        values = line.split(",")
        entradas.append([float(v) for v in values[:4]])
        saidas.append(int(values[4]))
    
    f.close()

    print(entradas)
    print(saidas)
    
    return (entradas,saidas)


CLASSES = [0,1]
INPUT_VARS = ["variance", "skewness", "curtosis", "entropy"]
LING_VALUES = ["low", "medium", "high"]

#funcoes de pertinencia

def default_pertinence_low(x):
    if x <= 0.2:
        return 1.
    elif x <= 0.4:
        return 1 - (x-0.2)/0.2
    else: 
        return 0.

def default_pertinence_medium(x):
    if x >= 0.3 and x <= 0.5:
        return (x-0.4)/0.4
    elif x <= 0.4:
        return 1 - (x-0.2)/0.2
    else: 
        return 0.

