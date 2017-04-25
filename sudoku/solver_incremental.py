#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import bisect
import threading

TENTATIVAS = 5000

class Node :
    def __init__( self, data ) :
        self.data = data
        self.next = None
        self.prev = None




class FilaPrioridadeLimitada():
    
    def __init__(self, maxsize):
        self.queue = []
        self.mutex = threading.Lock()
        self.maxsize = maxsize
        


    def __len__(self):
        return len(self.queue);
    
    def __iter__(self):
        return self.queue.__iter__()

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
        itens = [item for item in self.queue]
        self.queue = []
        return itens

            
    def last(self):
        self.mutex.acquire()
        last = self.queue[-1]
        self.mutex.release()
        return last
    
    
    

class Solver:
    
    def __init__(self, tabInicial, k):
        self.vizinhos = FilaPrioridadeLimitada(k)
        self.tabInicial = tabInicial
        self.k = k
        self.visitados = []
        self.countErrors = 0
#         self.temperatura = 
    
    def checkVisitados(self, tab, lin, col):

        if tab.matriz in self.visitados:
            tab.unflip(lin,col)
            return False
        return True
    
    def dontCheckVisitados(self, tab, lin, col):
        return True 
    
    
    def preencheProximo1a9(self, tab, vizinhosAtuais):
        for i in range(9):
            proximo = tab.preencheProximo(i)
            if proximo:
                proximo.setFitness(81-proximo.contPreenchidos())
                self.vizinhos.put(proximo)



    def preencheProximoRandom(self, tab, vizinhosAtuais):
        for i in range(9):
            proximo = tab.preencheProximoRandom()
            if proximo:
                proximo.setFitness(81-proximo.contPreenchidos())
                self.vizinhos.put(proximo)
            else:
                estadoInicial = self.tabInicial.preencheAlgumEmBranco(random.randrange(9))
                if estadoInicial:
                    estadoInicial.setFitness(81 - estadoInicial.contPreenchidos())
                    self.vizinhos.put(estadoInicial)
            
    def preencheAlgumBranco(self, tab, vizinhosAtuais):
        # for i in range(9):
        proximo = tab.preencheAlgumEmBranco(random.randrange(9))
        if proximo:
            proximo.setFitness(81-proximo.contPreenchidos())
            self.vizinhos.put(proximo)
        
        
        

    def resolver_sudoku_paralelo(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAlgumEmBranco(random.randrange(9))
            if estadoInicial:
                estadoInicial.setFitness(81-estadoInicial.contPreenchidos())
                self.vizinhos.put(estadoInicial)
#             self.visitados.append(estadoInicial)
        
        tentativas = 0
        while True:
            
            melhor = self.vizinhos.get()
            if melhor.estahResolvido() or tentativas == TENTATIVAS:
                return melhor
            self.vizinhos.put(melhor)
            print(melhor.getFitness())
            
            vizinhosAtuais = self.vizinhos.getAll()

            threads = []
            for v in vizinhosAtuais:
                t = threading.Thread(target=metodoVizinhos, kwargs = {"tab":v, "vizinhosAtuais":vizinhosAtuais} )
                t.daemon = True
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
            
            tentativas += 1
            print(tentativas)
            print("Quant vizinhos: ", len(self.vizinhos))
            
    def resolver_sudoku_sequencial(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAlgumEmBranco(random.randrange(9))
            if estadoInicial and not estadoInicial.matriz in [v.matriz for v in self.vizinhos]:
                estadoInicial.setFitness(81-estadoInicial.contPreenchidos())
                self.vizinhos.put(estadoInicial)
#             self.visitados.append(estadoInicial)
        
        tentativas = 0
        while True:
            
            melhor = self.vizinhos.get()
            if melhor.estahResolvido() or tentativas == TENTATIVAS:
                return melhor
            self.vizinhos.put(melhor)
            print(melhor.getFitness())
            
            vizinhosAtuais = self.vizinhos.getAll()

            for v in vizinhosAtuais:
                metodoVizinhos(v, vizinhosAtuais)
            
            tentativas += 1
            print(tentativas)
            print("Quant vizinhos: ", len(self.vizinhos))
            
            
                
        
       
           
       

# 
# t_inicial = time.time()
# 
# print_matriz(resolver_sudoku(TAB_MAIS_DIFICIL_DO_MUNDO))
# 
# t_final = time.time()
# print "Tempo de execução =", t_final - t_inicial

solver = Solver(TAB_TAREFA,100)
solucao = solver.resolver_sudoku_sequencial(solver.preencheProximoRandom  )
solucao.printthis()
print(solucao.fitness)