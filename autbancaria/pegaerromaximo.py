FILENAME = "erro.txt"


def lerArquivo():
    f = open(FILENAME, "r")

    dados = []
    for line in f.readlines():
        values = line.split(";")
        print(values)
        value = values[-2]
        value.strip()
        value = value.split(" ")[-1]
        print(value)
        value = value.replace(",",".")
        print(value)
        value = abs(float(value))
        dados.append(value)

    f.close()

    return dados


DADOS = lerArquivo()
print(max(DADOS))
acertos = [d for d in DADOS if d < 0.5]
print (len(acertos)/len(DADOS))