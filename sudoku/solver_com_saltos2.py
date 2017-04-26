#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import bisect
import threading
import math

TENTATIVAS = 10000

def scale_value(x,minimo = 0,maximo = math.e):
	    return (x - minimo) / (maximo - minimo)

def transf_e(x):
	return math.e**x

def tempera(x):
	return scale_value(transf_e(1-x))

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class FilaPrioridadeLimitada():
    def __init__(self, maxsize):
        self.queue = []
        self.mutex = threading.Lock()
        self.maxsize = maxsize

    def __len__(self):
        return len(self.queue)

    def put(self, item):
        self.mutex.acquire()
        if len(self.queue) == self.maxsize:
            self.queue = self.queue[:-1]

        bisect.insort(self.queue, item)
        self.mutex.release()

    def get(self):
        self.mutex.acquire()
        item = self.queue.pop(0)
        self.mutex.release()
        return item

    def getAll(self):
        return [item for item in self.queue]

    def last(self):
        self.mutex.acquire()
        last = self.queue[-1]
        self.mutex.release()
        return last

    def removeRandom(self):
        self.mutex.acquire()
        value = self.queue[random.randrange(len(self.queue))]
        self.queue.remove(value)
        self.mutex.release()

    def removeLast(self):
        self.mutex.acquire()
        self.queue = self.queue[:-1]
        self.mutex.release()

    def removeAll(self):
        self.queue = []

    def __iter__(self):
        return self.queue.__iter__()


class Solver:
    def __init__(self, tabInicial, k):
        self.vizinhos = FilaPrioridadeLimitada(k)
        self.tabInicial = tabInicial
        self.k = k
        self.visitados = []
        self.countErrors = 0
        self.tentativas = 0
        import sys
        self.melhor = sys.maxsize
        self.contaMelhorSemProgredir = 0
        self.limite_estagnacao = 500
        self.porcentagem_limpa = 0.99
        self.porcentagem_novos = 0.01
        self.aleatoriedade = True
        self.considera_visitados = False
        self.file = open("melhores.csv", "w")
        self.count_calc_fitness = 0

    #         self.temperatura =

    def checkVisitados(self, tab, lin, col):

        if tab.matriz in self.visitados:
            tab.unflip(lin, col)
            return False
        return True

    def dontCheckVisitados(self, tab, lin, col):
        return True

    def tryByFlip(self, tab, lin, col, vizinhosAtuais, checkVisitados=checkVisitados):
        tab.flip(lin, col)
        if not checkVisitados(self, tab, lin, col):
            return
        fitness = tab.countInvalidos()
        try:
            if fitness < vizinhosAtuais[-1].getFitness():
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                self.vizinhos.put(novoTab)
                self.visitados.append(copy.deepcopy(novoTab.matriz))
        except IndexError:
            self.countErrors += 1
            print("erro")
        finally:
            tab.unflip(lin, col)

    def proximos_vizinhos_fliptodos(self, tab, vizinhosAtuais):

        for lin in range(9):
            for col in range(9):
                if (lin, col) not in tab.preenchidos:
                    self.tryByFlip(tab, lin, col, vizinhosAtuais, \
                                   self.checkVisitados if self.considera_visitados \
                                       else self.dontCheckVisitados())

    def proximos_vizinhos_flip_um_por_linha_random(self, tab, vizinhosAtuais):
        for lin in range(9):

            col = random.randrange(0, 9)
            while (lin, col) in tab.preenchidos:
                col = random.randrange(0, 9)

            self.tryByFlip(tab, lin, col, vizinhosAtuais, \
                           self.checkVisitados if self.considera_visitados \
                               else self.dontCheckVisitados())

    def proximos_vizinhos_flip_random(self, tab, vizinhosAtuais):

        # for i in range(9):
        lin, col = (random.randrange(0, 9), random.randrange(0, 9))
        while (lin, col) in tab.preenchidos:
            col = random.randrange(0, 9)

        self.tryByFlip(tab, lin, col, vizinhosAtuais, \
                       self.checkVisitados if self.considera_visitados \
                           else self.dontCheckVisitados())

    def proximos_vizinhos_total_random(self, tab, vizinhosAtuais):

        # for i in range(9):
        lin, col = (random.randrange(0, 9), random.randrange(0, 9))
        while (lin, col) in tab.preenchidos:
            col = random.randrange(0, 9)

        randomnum = random.randrange(1, 10)
        anterior = tab[lin][col]
        tab[lin][col] = randomnum

        try:
            if self.considera_visitados and tab.matriz in self.visitados:
                tab[lin][col] = anterior
                return

            fitness = tab.countInvalidos()  ##Função objetivo
            self.count_calc_fitness += 1

            if self.aleatoriedade and random.random() >= self.tentativas / TENTATIVAS:
                for i in range(1): self.vizinhos.removeRandom()
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                self.vizinhos.put(novoTab)
                if self.considera_visitados:
                    self.visitados.append(copy.deepcopy(novoTab.matriz))
            elif vizinhosAtuais[-1] and fitness < vizinhosAtuais[-1].getFitness():
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                tab[lin][col] = anterior
                if novoTab.matriz not in [tab.matriz for tab in self.vizinhos]:
                    self.vizinhos.put(novoTab)
                    if self.considera_visitados:
                        self.visitados.append(copy.deepcopy(novoTab.matriz))



        # except IndexError: print("erro")
        finally:
            tab[lin][col] = anterior

    def proximo_vizinhos_random_9(self, tab, vizinhosAtuais):
        for i in range(9):
            self.proximos_vizinhos_total_random(tab, vizinhosAtuais)

    def resolver_sudoku_paralelo(self, metodoVizinhos):
        self.preparacao_inicial()
        while True:

            melhor = self.vizinhos.get()
            if melhor.estahResolvido() or self.tentativas == TENTATIVAS:
                return melhor
            self.vizinhos.put(melhor)
            print(melhor.getFitness())

            vizinhosAtuais = self.resolver_parte1(melhor)

            threads = []
            for v in vizinhosAtuais:
                t = threading.Thread(target=metodoVizinhos, kwargs={"tab": v, "vizinhosAtuais": vizinhosAtuais})
                t.daemon = True
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            self.resolver_parte2()

    def resolver_parte1(self, melhor):


        if self.aleatoriedade:
            if melhor.getFitness() < self.melhor:
                self.melhor = melhor.getFitness()
                self.contaMelhorSemProgredir = 0
            else:
                self.contaMelhorSemProgredir += 1

            if self.contaMelhorSemProgredir > self.limite_estagnacao:
                for i in range(int(self.k * self.porcentagem_limpa)): self.vizinhos.removeRandom()
                for i in range(int(self.k * self.porcentagem_limpa)):

                    estadoAleatorio = self.tabInicial.preencheAleatorio()
                    if estadoAleatorio.matriz not in self.visitados:
                        self.vizinhos.put(estadoAleatorio)
                        if self.considera_visitados:
                            self.visitados.append(copy.deepcopy(estadoAleatorio.matriz))
                self.contaMelhorSemProgredir = 0

        vizinhosAtuais = self.vizinhos.getAll()
        return vizinhosAtuais

    def resolver_parte2(self):

        print("Num de visitados:", len(self.visitados))
        print("Num de vizinhos:", len(self.vizinhos))
        self.tentativas += 1
        print(self.tentativas)

    def preparacao_inicial(self):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAleatorio()
            self.vizinhos.put(estadoInicial)
            if self.considera_visitados:
                self.visitados.append(copy.deepcopy(estadoInicial.matriz))

        self.tentativas = 0

    def resolver_sudoku_sequencial(self, metodoVizinhos):


        try:
            self.preparacao_inicial()
            while True:

                melhor = self.vizinhos.get()
                if melhor.estahResolvido() or self.tentativas == TENTATIVAS:
                    return melhor
                self.vizinhos.put(melhor)
                print(melhor.getFitness())
                self.file.write(str(melhor.getFitness())+"\n")

                vizinhosAtuais = self.resolver_parte1(melhor)

                for v in vizinhosAtuais:
                    metodoVizinhos(v, vizinhosAtuais)

                self.resolver_parte2()

        finally:
            self.file.close()



opcao = int(input("Default (1) ou Customizado (2)? "))
if opcao == 1:
    solver = Solver(TAB_TAREFA, 1000)
    solucao = solver.resolver_sudoku_sequencial(solver.proximos_vizinhos_total_random)

else:
    k = int(input("Valor do k: "))
    solver = Solver(TAB_TAREFA, k)

    modos_execucao = [solver.resolver_sudoku_sequencial, solver.resolver_sudoku_paralelo]
    estrategias_vizinho = [solver.proximos_vizinhos_total_random, solver.proximos_vizinhos_fliptodos, \
                           solver.proximos_vizinhos_flip_um_por_linha_random, \
                           solver.proximos_vizinhos_flip_random]

    modo_exec = modos_execucao[int(input("Sequencial (1) ou Paralelo (2): ")) - 1]
    estrat_vizinho = estrategias_vizinho[
        int(input("Áleatório total (1), Flip todos (2), Flip um por linha (3), ou Flip Aleatório (4)")) - 1]
    TENTATIVAS = int(input("Quantas iterações: "))

    solver.considera_visitados = True if int(input("Considera visitados (1) ou Não (2): ")) == 1 else False


    solver.aleatoriedade = True if int(input("Aleatoriedade (1) ou Não (2): ")) == 1 else False

    if solver.aleatoriedade:
        porcentagem_novos = float(input("Porcentagem de novos aleaórios: "))
        limite_estagnacao = int(input("Limite de estagnação: "))
        porcentagem_limpa_estagnacao = float(input("Porcentagem de limpa ao estagnar: "))

        solver.porcentagem_limpa = porcentagem_limpa_estagnacao
        solver.limite_estagnacao = limite_estagnacao
        solver.porcentagem_novos = porcentagem_novos

    solucao = modo_exec(estrat_vizinho)

solucao.printthis()
print(solucao.fitness)
print("Avaliações de função objetivo =", solver.count_calc_fitness)