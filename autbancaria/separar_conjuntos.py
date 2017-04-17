FILENAME = "dados_autent_bancaria.txt"

def lerArquivo():
    f = open(FILENAME,"r")
    
    dados = []
    
    for line in f:
        values = line.split(",")
        dados.append([float(v) for v in values])
    
    f.close()
    
    return dados

DADOS = lerArquivo()

DADOSCLASS0 = [d for d in DADOS if d[4] == 0.]
DADOSCLASS1 = [d for d in DADOS if d[4] == 1.]

NC0 = len(DADOSCLASS0)
NC1 = len(DADOSCLASS1)
NC0Train = int(NC0*0.8)
NC0Test = int(NC0*0.2)
NC1Train = int(NC1*0.8)
NC1Test = int(NC1*0.2)

print(NC0)
print(NC1)

DADOSCLASS0TRAIN = DADOSCLASS0[:NC0Train]
DADOSCLASS0TEST = DADOSCLASS0[NC0Train:]

DADOSCLASS1TRAIN = DADOSCLASS1[:NC1Train]
DADOSCLASS1TEST = DADOSCLASS1[NC1Train:]

print(len(DADOSCLASS0TRAIN))
print(len(DADOSCLASS0TEST))
print(len(DADOSCLASS1TRAIN))
print(len(DADOSCLASS1TEST))

FILETRAIN = "dadostrain.txt"
FILETEST = "dadostest.txt"

ftrain = open(FILETRAIN, "w")
ftest = open(FILETEST, "w")

for dados in DADOSCLASS0TRAIN + DADOSCLASS1TRAIN:
    dados = [str(d) for d in dados]
    ftrain.write(dados[0]+","+dados[1]+","+dados[2]+","+dados[3]+","+dados[4]+"\n")
    
for dados in DADOSCLASS0TEST+DADOSCLASS1TEST:
    dados = [str(d) for d in dados]
    ftest.write(dados[0]+","+dados[1]+","+dados[2]+","+dados[3]+","+dados[4]+"\n")
    
ftrain.close()
ftest.close()
