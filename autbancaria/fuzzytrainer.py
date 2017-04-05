from numpy.core.defchararray import index
from compiler.ast import Class


################## PREPARACAO ##################

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

ENTRADAS, SAIDAS = lerArquivo()

CLASSES = ["falsificada", "autentica"]
INPUT_VARS = ["variance", "skewness", "curtosis", "entropy"]
LING_VALUES = ["low", "medium", "high"]


MAXVARS = []
MINVARS = []
def calculaMaxEMins():
    
    for i in range(len(INPUT_VARS)):
        varss =  [entrada[i] for entrada in ENTRADAS]
        maxvar = max(varss)
        minvar = min(varss)
        MAXVARS.append(maxvar)
        MINVARS.append(minvar)
        
    print MAXVARS
    print MINVARS
    
calculaMaxEMins()


################# funcoes de pertinencia (grid uniforme) #################

def scale_value(x,minimo,maximo):
    return (x - minimo) / (maximo - minimo)

print(scale_value(4.5459, -7.0421, 6.8248))
print(scale_value(0.1, 0, 1))

def gen_default_pertinence_low(minimo,maximo):
    
    def pertinence_low(x):
        x = scale_value(x, minimo, maximo)
        if x <= 0.2:
            return 1.
        elif x <= 0.4:
            return 1 - (x-0.2)/0.2
        else: 
            return 0.
#     
#     assert pertinence_low(0.1) == 1
#     assert pertinence_low(0.2) == 1
#     assert isclose(pertinence_low(0.3),0.5)
#     assert pertinence_low(0.4) == 0
#     assert pertinence_low(0.5) == 0
#         
        
    return pertinence_low



def gen_default_pertinence_medium(minimo, maximo):
    def pertinence_medium(x):
        x = scale_value(x, minimo, maximo)
        if x >= 0.3 and x <= 0.5:
            return (x - 0.3) / 0.2
        elif x > 0.5 and x <= 0.7:
            return 1 - ((x - 0.5) / 0.2)
        else: 
            return 0.
        
#     assert pertinence_medium(0.2) == 0.
#     assert pertinence_medium(0.4) == (0.4 - 0.3) / 0.2
#     assert pertinence_medium(0.6) == 1 - ((0.6 - 0.5) / 0.2)
#     assert pertinence_medium(0.7) == 1 - ((0.7 - 0.5) / 0.2)
#     assert pertinence_medium(0.5) == ((0.5 - 0.3) / 0.2)

    return pertinence_medium


def gen_default_pertinence_high(minimo, maximo):
    def pertinence_high(x):
        x = scale_value(x, minimo, maximo)
        if x >= 0.6 and x <= 0.8:
            return (x - 0.6) / 0.2
        elif x > 0.8:
            return 1.
        else: 
            return 0.
    
#     assert pertinence_high(0.7) == (0.7 - 0.6) / 0.2
#     assert pertinence_high(0.6) == (0.6 - 0.6) / 0.2
#     assert pertinence_high(0.9) == 1.    
        
    return pertinence_high

    
PERT_FUNCTIONS_GENS = [gen_default_pertinence_low, gen_default_pertinence_medium, gen_default_pertinence_high]

PERT_FUNCTIONS = []

def generate_pertinence_functions():
    for v in range(len(INPUT_VARS)):
        var_functions = []
        for k in range(len(LING_VALUES)):
            gen = PERT_FUNCTIONS_GENS[k]
            func = gen(MINVARS[v], MAXVARS[v])
            var_functions.append(func)
        PERT_FUNCTIONS.append(var_functions)

generate_pertinence_functions()

print PERT_FUNCTIONS



######################## Criar regras basicas ###########################

def calcRegras():
        
    regras = []
    for entrada, saida in zip(ENTRADAS, SAIDAS):
        termos = []
        
        for i in range(len(entrada)):
            pertinencias = []
            
            for pertf in PERT_FUNCTIONS[i]:
                pert = pertf(entrada[i])
                pertinencias.append(pert)
                
            maior = max(pertinencias)
            index_maior = pertinencias.index(maior)
            lingValue = LING_VALUES[index_maior]
            termos.append((lingValue,maior))
            
        termos.append(CLASSES[saida])
        regras.append(termos)
        
    return regras

        
def printRegras(regras):
    for r in regras:
        print "Se",
        for i in range(len(INPUT_VARS)):
            print INPUT_VARS[i],"=", r[i],
            if i != len(INPUT_VARS) - 1: print "e",
        print "entao",r[4]
             

regras = calcRegras()
printRegras(regras)


###################### Calcular niveis de disparo ########################

# norma-t por minimo
def norma_t(pertlist):
    return min(pertlist)


niveis_disparos = []
for r in regras:
    nivel = norma_t([t[1] for t in r[:4]])
    niveis_disparos.append(nivel)
    
print niveis_disparos

###################### encontrar antecedentes iguais #################

antecedentes = {}

for i in range(len(regras)):
    ante = tuple([regras[i][v][0] for v in range(len(INPUT_VARS))])
    if ante not in antecedentes.keys():
        antecedentes[ante] = [i]
    else:
        antecedentes[ante].append(i)

print antecedentes

##################### filtrar regras pelo antecedente com maior regra de disparo ################

regras_finais = []
for ante, indices in antecedentes.iteritems():
    
    max_nivel_disparo = max([niveis_disparos[i] for i in indices])
    indice_max = niveis_disparos.index(max_nivel_disparo)
    
    regra = regras[indice_max]
    regras_finais.append(regra)
    

printRegras(regras_finais)
print len(regras)
print len(regras_finais)
        
                     







