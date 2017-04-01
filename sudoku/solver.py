#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import time
import bisect
import random
from Queue import Queue
import threading

TENTATIVAS = 200000

class FilaPrioridadeLimitada():
    
    def __init__(self, maxsize):
        self.queue = []
        self.mutex = threading.Lock()
        self.maxsize = maxsize
        self.len = 0


    def put(self, item):
        self.mutex.acquire()
        self.queue = self.queue[:-1]
        
                    #         if len(self.queue) == self.maxsize:
        #             last = self._queue.pop()
        # #             if last < item:
        # #                 self.queue.append(last)
        # #                 return
        
        bisect.insort(self.queue, item)
        self.len+=1
        self.mutex.release()
        
    
    def get(self):
        self.mutex.acquire()
        item = self.queue.pop(0)
        self.len-=1
        self.mutex.release()
        return item
    
    
   
    def getAll(self):
        return [item for item in self.queue]

            
    def last(self):
        self.mutex.acquire()
        last = self.queue[self.len-1]
        self.mutex.release()
        return last
    
    
    

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
                    if fitness < self.vizinhos.last().getFitness():                       
                        novoTab = tab.clone()
                        novoTab.setFitness(fitness)
                        self.vizinhos.removeLast()
                        self.vizinhos.put(novoTab)
                    tab.unflip(lin,col)


    def proximos_vizinhos_flip_um_por_linha_random(self,tab):
        for lin in range(9):
            
            col = random.randrange(0,9)
            while (lin,col) in tab.preenchidos:
                col = random.randrange(0,9)

            tab.flip(lin,col)
            fitness = tab.countInvalidos()
            if fitness < self.vizinhos.last().getFitness():                       
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                self.vizinhos.put(novoTab)
            tab.unflip(lin,col)
            
            
    def proximos_vizinhos_flip_total_random(self,tab,vizinhosAtuais):     
            
        #for i in range(9):
        lin,col = (random.randrange(0,9),random.randrange(0,9))
        while (lin,col) in tab.preenchidos:
            col = random.randrange(0,9)

        randomnum = random.randrange(1,10)
        anterior = tab[lin][col]
        tab[lin][col] = randomnum
        fitness = tab.countInvalidos()
        try:
            if fitness < vizinhosAtuais[-1].getFitness():                       
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                self.vizinhos.put(novoTab)
        #except IndexError: print("erro")
        finally:
            tab[lin][col] = anterior


    def resolver_sudoku(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAleatorio()
            self.vizinhos.put(estadoInicial)
        
        tentativas = 0
        while True:
            
            melhor = self.vizinhos.get()
            if melhor.estahResolvido() or tentativas == TENTATIVAS:
                return melhor
            self.vizinhos.put(melhor)
            
            vizinhosAtuais = self.vizinhos.getAll()

            for v in vizinhosAtuais:
                t = threading.Thread(target=self.proximos_vizinhos_flip_total_random, kwargs = {"tab":v, "vizinhosAtuais":vizinhosAtuais} )
                t.daemon = True
                t.start()
            
            tentativas += 1
            print(tentativas)
            
                
        
       
           
       

# 
# t_inicial = time.time()
# 
# print_matriz(resolver_sudoku(TAB_MAIS_DIFICIL_DO_MUNDO))
# 
# t_final = time.time()
# print "Tempo de execução =", t_final - t_inicial

solver = Solver(TAB_TAREFA,1000)
solucao = solver.resolver_sudoku(solver.proximos_vizinhos_flip_um_por_linha_random)
solucao.printthis()
print(solucao.fitness)