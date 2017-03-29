#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import time
import bisect
import random

TENTATIVAS = 100

class FilaPrioridadeLimitada:
    
    def __init__(self, maxlen=-1):
        self._queue = []
        self._maxlen = maxlen
        
    def get(self,i):
        return self._queue[i]
        
    def pop(self):
        return self._queue.pop(0)
    
    def put(self,item):
        if len(self._queue) == self._maxlen:
            last = self._queue.pop()
            if last < item:
                self._queue.append(last)
                return
        
        bisect.insort(self._queue, item)
            
    def last(self):
        return self._queue[len(self._queue)-1]       
    
    

class Solver:
    
    def __init__(self, tabInicial, k):
        self.vizinhos = FilaPrioridadeLimitada(k)
        self.tabInicial = tabInicial
        self.k = k
        
    
    def proximos_vizinhos_fliptodos(self, tab):
           
        for lin in range(9):
            for col in range(9):
                if (lin,col) not in tab.preenchidos:
                    tab.flip(lin,col)
                    fitness = tab.countInvalidos()
                    if fitness < tab.getFitness() and fitness < self.vizinhos.last().getFitness():                       
                        novoTab = tab.clone()
                        novoTab.setFitness(fitness)
                        self.vizinhos.put(novoTab)
                    tab.unflip(lin,col)


    def proximos_vizinhos_flip_um_por_linha_random(self,tab):
        for lin in range(9):
            
            col = random.randrange(0,9)
            while (lin,col) in tab.preenchidos:
                col = random.randrange(0,9)

            tab.flip(lin,col)
            fitness = tab.countInvalidos()
            if fitness < tab.getFitness() and fitness < self.vizinhos.last().getFitness():                       
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                self.vizinhos.put(novoTab)
            tab.unflip(lin,col)

    def resolver_sudoku(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAleatorio()
            self.vizinhos.put(estadoInicial)
        
        tentativas = 0
        while True:
            
            if self.vizinhos.get(0).estahResolvido() or tentativas == TENTATIVAS:
                return self.vizinhos.pop()
            
            vizinhosAtuais = []
            
            for i in range(self.k):                
                v = self.vizinhos.get(i)
                vizinhosAtuais.append(v)

            for v in vizinhosAtuais:
                metodoVizinhos(v)
            
            tentativas += 1
            print(tentativas)
            
                
        
       
           
       

# 
# t_inicial = time.time()
# 
# print_matriz(resolver_sudoku(TAB_MAIS_DIFICIL_DO_MUNDO))
# 
# t_final = time.time()
# print "Tempo de execução =", t_final - t_inicial

solver = Solver(TAB_TAREFA,100)
solucao = solver.resolver_sudoku(solver.proximos_vizinhos_flip_um_por_linha_random)
solucao.printthis()
print(solucao.fitness)