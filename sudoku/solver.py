#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sudoku.dados import *
import time
import bisect

TENTATIVAS = 5000

class Solver:
    
    def __init__(self, tabInicial, k):
        self.vizinhos = []
        self.tabInicial = tabInicial
        self.k = k
        
    
    def proximos_vizinhos(self, tab):
        '''
        :param tab: Tabuleiro
        :return: List[Tabuleiro]
        '''      
        for lin in range(9):
            for col in range(9):
                if (lin,col) not in tab.preenchidos:
                    novoTab = tab.clone()
                    novoTab.flip(lin,col)
                    novoTab.countInvalidos()
                    bisect.insort(self.vizinhos, novoTab)


    def resolver_sudoku(self):
        for i in range(self.k):
            bisect.insort(self.vizinhos, self.tabInicial.preencheAleatorio())
        
        tentativas = 0
        while True:
            
            vizinhosAtuais = []
            
            for i in range(self.k):
                v = self.vizinhos.pop(0)
                if v.estahResolvido() or tentativas == TENTATIVAS:
                    return v
                vizinhosAtuais.append(v)
            
            
            self.vizinhos = []
            
            for v in vizinhosAtuais:
                self.proximos_vizinhos(v)
            
            tentativas += 1
                
        
       
           
       

# 
# t_inicial = time.time()
# 
# print_matriz(resolver_sudoku(TAB_MAIS_DIFICIL_DO_MUNDO))
# 
# t_final = time.time()
# print "Tempo de execução =", t_final - t_inicial

solver = Solver(TAB_TAREFA,10)
solucao = solver.resolver_sudoku()
solucao.printthis()