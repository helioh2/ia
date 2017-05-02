

class CalcRegras():

    def __init__(self, entradas, saidas, pert_functions, ling_values, classes, input_vars):
        self.entradas = entradas
        self.saidas = saidas
        self.pert_functions = pert_functions
        self.ling_values = ling_values
        self.classes = classes
        self.input_vars = input_vars
        self.regras_basicas = []
        self.regras_finais = []

    def calcRegrasBasicas(self):
        for entrada, saida in zip(self.entradas, self.saidas):
            termos = []

            for i in range(len(entrada)):
                pertinencias = []

                for pertf in self.pert_functions[i]:
                    pert = pertf(entrada[i])
                    pertinencias.append(pert)

                maior = max(pertinencias)
                index_maior = pertinencias.index(maior)
                lingValue = self.ling_values[index_maior]
                termos.append((lingValue, maior))

            termos.append(self.classes[int(saida)])
            self.regras_basicas.append(termos)



    def printRegras(self,regras):
        for r in regras:
            print("Se", end=" ")
            for i in range(len(self.input_vars)):
                print(self.input_vars[i], "=", r[i], end=" ")
                if i != len(self.input_vars) - 1: print("e", end=" ")
            print("entao", r[4])


# regras = calcRegras(ENTRADAS, SAIDAS)
# printRegras(regras)


###################### Calcular niveis de disparo ########################

    def produtorio(L):
        res = 1
        for item in L:
            res *= item
        return res

    def calcula_niveis_disparo(self, norma_t=min):
        niveis_disparos = []
        for r in self.regras_basicas:
            nivel = norma_t([t[1] for t in r[:4]])
            niveis_disparos.append(nivel)
        return niveis_disparos



# niveis_disparos = calcula_niveis_disparo(min) #norma-t = min
# niveis_disparos = calcula_niveis_disparo(produtorio)  # norma-t = produtorio
# print(niveis_disparos)

###################### encontrar antecedentes iguais #################
    def encontraAntecedentesIguais(self):
        antecedentes = {}

        for i in range(len(self.regras_basicas)):
            ante = tuple([self.regras_basicas[i][v][0] for v in range(len(self.input_vars))])
            if ante not in antecedentes.keys():
                antecedentes[ante] = [i]
            else:
                antecedentes[ante].append(i)

        return antecedentes

##################### filtrar regras pelo antecedente com maior regra de disparo ################
    def calcula_regras_finais(self):
        self.calcRegrasBasicas()
        antecedentes = self.encontraAntecedentesIguais()
        niveis_disparos = self.calcula_niveis_disparo()
        for ante, indices in antecedentes.items():
            max_nivel_disparo = max([niveis_disparos[i] for i in indices])
            indice_max = niveis_disparos.index(max_nivel_disparo)

            regra = self.regras_basicas[indice_max]
            self.regras_finais.append(regra)

        print("----------Regras Finais: -------------")
        self.printRegras(self.regras_finais)
        print("----------------Fim Regras Finais------------------------------")
        print("Quantidade de regras básicas =",len(self.regras_basicas))
        print("Quantidade de regras finais =",len(self.regras_finais))
        return self.regras_finais
