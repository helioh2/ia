#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import bisect
import threading

TENTATIVAS = 10000

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
    
    def removeLast(self):
        
      
        self.mutex.acquire()
        self.queue = self.queue[:-1]
        self.mutex.release()
        
    def removeRandom(self):
        
        self.mutex.acquire()
        value = self.queue[random.randrange(len(self.queue))]
        self.queue.remove(value)
        self.mutex.release()
        
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
#         self.temperatura = 
    
    def checkVisitados(self, tab, lin, col):

        if tab.matriz in self.visitados:
            tab.unflip(lin,col)
            return False
        return True
    
    def dontCheckVisitados(self, tab, lin, col):
        return True 
    
    def tryByFlip(self, tab, lin, col, vizinhosAtuais, checkVisitados = checkVisitados):
        tab.flip(lin,col)
        if not checkVisitados(self,tab,lin,col):
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
            tab.unflip(lin,col)
            
    
    
    def proximos_vizinhos_fliptodos(self, tab, vizinhosAtuais):
           
        for lin in range(9):
            for col in range(9):
                if (lin,col) not in tab.preenchidos:
                    self.tryByFlip(tab, lin, col, vizinhosAtuais)


    def proximos_vizinhos_flip_um_por_linha_random(self,tab, vizinhosAtuais):
        for lin in range(9):
            
            col = random.randrange(0,9)
            while (lin,col) in tab.preenchidos:
                col = random.randrange(0,9)

            self.tryByFlip(tab, lin, col, vizinhosAtuais)
    
    def proximos_vizinhos_flip_random(self,tab,vizinhosAtuais):     
            
        #for i in range(9):
        lin,col = (random.randrange(0,9),random.randrange(0,9))
        while (lin,col) in tab.preenchidos:
            col = random.randrange(0,9)
            
        self.tryByFlip(tab, lin, col, vizinhosAtuais)
        
    
    def proximos_vizinhos_total_random(self,tab,vizinhosAtuais):     
            
        #for i in range(9):
        lin,col = (random.randrange(0,9),random.randrange(0,9))
        while (lin,col) in tab.preenchidos:
            col = random.randrange(0,9)

        randomnum = random.randrange(1,10)
        anterior = tab[lin][col]
        tab[lin][col] = randomnum
        
        try:
#             if tab.matriz in self.visitados:
#                 tab[lin][col] = anterior
#                 return
        
            fitness = tab.countInvalidos()
            
            if fitness < vizinhosAtuais[-1].getFitness():                     
                novoTab = tab.clone()
                novoTab.setFitness(fitness)
                tab[lin][col] = anterior                 
#                 if not novoTab in self.visitados:                   
                self.vizinhos.put(novoTab)  
#                     self.visitados.append(novoTab)
            else:
                if random.random() >= 0.0:
                    novoTab = tab.clone()
                    novoTab.setFitness(fitness)
                    
#                     if not novoTab in self.visitados:                   
                        
                    if len(self.vizinhos) == self.vizinhos.maxsize:
<<<<<<< HEAD
                        for i in range(int(self.k*0.05)): self.vizinhos.removeRandom()
                    self.vizinhos.put(novoTab)
=======
                        for i in range(int(self.k*0.01)): self.vizinhos.removeRandom()
>>>>>>> branch 'master' of https://github.com/helioh2/ia.git
                    
                    
                    self.vizinhos.put(novoTab)
                
#                     self.visitados.append(novoTab)
                    
                
        #except IndexError: print("erro")
        finally:
            tab[lin][col] = anterior


    def proximo_vizinhos_random_9(self,tab, vizinhosAtuais):
        for i in range(9):
            self.proximos_vizinhos_total_random(tab, vizinhosAtuais)

    def resolver_sudoku_paralelo(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAleatorio()
            self.vizinhos.put(estadoInicial)
#             self.visitados.append(estadoInicial)
        
        self.tentativas = 0
        while True:
            
            melhor = self.vizinhos.get()
            if melhor.estahResolvido() or self.tentativas == TENTATIVAS:
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
            
            self.tentativas += 1
            print(self.tentativas)
            
    def resolver_sudoku_sequencial(self, metodoVizinhos):
        for i in range(self.k):
            estadoInicial = self.tabInicial.preencheAleatorio()
            self.vizinhos.put(estadoInicial)
            self.visitados.append(estadoInicial)
        
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
            
            
                
        
       
           
       

# 
# t_inicial = time.time()
# 
# print_matriz(resolver_sudoku(TAB_MAIS_DIFICIL_DO_MUNDO))
# 
# t_final = time.time()
# print "Tempo de execução =", t_final - t_inicial

solver = Solver(TAB_TAREFA,100)
solucao = solver.resolver_sudoku_sequencial(solver.proximos_vizinhos_total_random )
solucao.printthis()
print(solucao.fitness)