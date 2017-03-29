#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''Funcoes auxiliares:'''


def print_matriz(m):
    for l in range(len(m)):

        for c in range(len(m[l])):
            item = ""
            if m[l][c] == None:
                item += "B\t"
            else:
                item += str(m[l][c]) + "\t"
            if c == len(m[l]) - 1:
                item += "\n"
            print item,


'''
SUDOKU - ANALISE DE DOMINIO

Num tabuleiro de Sudoku, temos uma matriz 9x9
com 9 LINHAS, 9 COLUNAS, e tambem 9 CAIXAS 3x3
Vamos chamar as LINHAS, COLUNAS e CAIXAS de Unidades,
pois a ideia do Sudoku eh atribuir valores (Natural[1,9]) dentro dessas unidades
de modo que nao quebre a restricao de nao repetir valores em cada
unidade. Portanto, teremos 27 Unidades no total (9 LINHAS, 9 COLUNAS e 9 CAIXAS)
'''

'''
DEFINICAO DOS DADOS:
----
Valor eh Natural[1,9]
----

----
Tabuleiro eh uma Matriz[0..8, 0..8] de (Valor ou None) 
interp. uma matriz 9x9 que representa um tabuleiro de Sudoku.
Cada posicao da lista pode conter um valor ou None caso ainda nao haja valor.
Uma matriz nada mais eh que uma lista de listas (ou vetor de vetores).

----

----
Posicao eh uma Tupla(0..8, 0..8)
interp. representa uma posicao no tabuleiro
----

----
Unidade eh uma Lista de Posicao de tamanho 9
interp. representa a posicao de cada quadrado em uma Unidade.
Ha 27 unidades: 9 linhas, 9 colunas e 9 caixas 
----

'''

''' Constantes e Exemplos: '''

# Definicao das Unidades e suas Posicao:

LINHAS = [[(l,c) for c in range(9)] for l in range(9)]
COLUNAS = [[(l,c) for l in range(9)] for c in range(9)]
CAIXAS = [[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)],
          [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)],
          [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
          [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)],
          [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)],
          [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
          [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)],
          [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)],
          [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]
           ]

UNIDADES = LINHAS + COLUNAS + CAIXAS
# print(UNIDADES)

#Exemplos de tabuleiros

TODOS_VALORES = range(1,10)  # Naturais de 1 a 9
B = None #valor nulo para facilitar os testes
TAB_VAZIO = [[None for _ in range(9)] for _ in range(9)]


TAB_L0_CHEIA = [TODOS_VALORES]+ [[None for _ in range(9)] for _ in range(8)]  #Matriz com primeira linha preenchida de 1 a 9
TAB_C0_CHEIA = [[valor]+[None]*8 for valor in TODOS_VALORES] #Matriz com primeira coluna preenchida de 1 a 9

# print_matriz(TAB_C0_CHEIA)

TAB_FACIL= [[2, 7, 4, B, 9, 1, B, B, 5],
            [1, B, B, 5, B, B, B, 9, B],
            [6, B, B, B, B, 3, 2, 8, B],
            [B, B, 1, 9, B, B, B, B, 8],
            [B, B, 5, 1, B, B, 6, B, B],
            [7, B, B, B, 8, B, B, B, 3],
            [4, B, 2, B, B, B, B, B, 9],
            [B, B, B, B, B, B, B, 7, B],
            [8, B, B, 3, 4, 9, B, B, B]]

TAB_FACIL_PROXIMO1= [[2, 7, 4, 1, 9, 1, B, B, 5],
                    [1, B, B, 5, B, B, B, 9, B],
                    [6, B, B, B, B, 3, 2, 8, B],
                    [B, B, 1, 9, B, B, B, B, 8],
                    [B, B, 5, 1, B, B, 6, B, B],
                    [7, B, B, B, 8, B, B, B, 3],
                    [4, B, 2, B, B, B, B, B, 9],
                    [B, B, B, B, B, B, B, 7, B],
                    [8, B, B, 3, 4, 9, B, B, B]]

TAB_FACIL_PROXIMO2 = [[2, 7, 4, 2, 9, 1, B, B, 5],
            [1, B, B, 5, B, B, B, 9, B],
            [6, B, B, B, B, 3, 2, 8, B],
            [B, B, 1, 9, B, B, B, B, 8],
            [B, B, 5, 1, B, B, 6, B, B],
            [7, B, B, B, 8, B, B, B, 3],
            [4, B, 2, B, B, B, B, B, 9],
            [B, B, B, B, B, B, B, 7, B],
            [8, B, B, 3, 4, 9, B, B, B]]

TAB_FACIL_SOLUCAO= [[2, 7, 4, 8, 9, 1, 3, 6, 5],
                    [1, 3, 8, 5, 2, 6, 4, 9, 7],
                    [6, 5, 9, 4, 7, 3, 2, 8, 1],
                    [3, 2, 1, 9, 6, 4, 7, 5, 8],
                    [9, 8, 5, 1, 3, 7, 6, 4, 2],
                    [7, 4, 6, 2, 8, 5, 9, 1, 3],
                    [4, 6, 2, 7, 5, 8, 1, 3, 9],
                    [5, 9, 3, 6, 1, 2, 8, 7, 4],
                    [8, 1, 7, 3, 4, 9, 5, 2, 6]]
                    
TAB_DIFICIL = [ [5, B, B, B, B, 4, B, 7, B],
                [B, 1, B, B, 5, B, 6, B, B],
                [B, B, 4, 9, B, B, B, B, B],
                [B, 9, B, B, B, 7, 5, B, B],
                [1, 8, B, 2, B, B, B, B, B],
                [B, B, B, B, B, 6, B, B, B],
                [B, B, 3, B, B, B, B, B, 8],
                [B, 6, B, B, 8, B, B, B, 9],
                [B, B, 8, B, 7, B, B, 3, 1]]    

TAB_DIFICIL_SOLUCAO = [ [5, 3, 9, 1, 6, 4, 8, 7, 2],
                        [8, 1, 2, 7, 5, 3, 6, 9, 4],
                        [6, 7, 4, 9, 2, 8, 3, 1, 5],
                        [2, 9, 6, 4, 1, 7, 5, 8, 3],
                        [1, 8, 7, 2, 3, 5, 9, 4, 6],
                        [3, 4, 5, 8, 9, 6, 1, 2, 7],
                        [9, 2, 3, 5, 4, 1, 7, 6, 8],
                        [7, 6, 1, 3, 8, 2, 4, 5, 9],
                        [4, 5, 8, 6, 7, 9, 2, 3, 1] ]

TAB_MAIS_DIFICIL_DO_MUNDO = [[B, B, 5, 3, B, B, B, B, B],
                            [8, B, B, B, B, B, B, 2, B],
                            [B, 7, B, B, 1, B, 5, B, B],
                            [4, B, B, B, B, 5, 3, B, B],
                            [B, 1, B, B, 7, B, B, B, 6],
                            [B, B, 3, 2, B, B, B, 8, B],
                            [B, 6, B, 5, B, B, B, B, 9],
                            [B, B, 4, B, B, B, B, 3, B],
                            [B, B, B, B, B, 9, 7, B, B]]

TAB_IMPOSSIVEL = [range(1,9)+[None]]+\
                    [[None]*8 + [valor] for valor in range(2,10)] #sem solucao, visualize dando um print nela
# print_matriz(TAB_IMPOSSIVEL)

TAB_INVALIDA1 = [[2, 7, 4, 2, 9, 1, B, B, 5],
                [1, B, B, 5, B, B, B, 9, B],
                [6, B, B, B, B, 3, 2, 8, B],
                [B, B, 1, 9, B, B, B, B, 8],
                [B, B, 5, 1, B, B, 6, B, B],
                [7, B, B, B, 8, B, B, B, 3],
                [4, B, 2, B, B, B, B, B, 9],
                [B, B, B, B, B, B, B, 7, B],
                [8, B, B, 3, 4, 9, B, B, B]]


TAB_MAIS_DIFICIL2 = [[8, B, B, B, B, B, B, B, B],
                    [B, B, 3, 6, B, B, B, B, B],
                    [B, 7, B, B, 9, B, 2, B, B],
                    [B, 5, B, B, B, 7, B, B, B],
                    [B, B, B, B, 4, 5, 7, B, B],
                    [B, B, B, 1, B, B, B, 3, B],
                    [B, B, 1, B, B, B, B, 6, 8],
                    [B, B, 8, 5, B, B, B, 1, B],
                    [B, 9, B, B, B, B, 4, B, B]]


def indicesPreenchidos(tab):
    return [(lin,col) for lin in range(9) for col in range(9) \
            if tab[lin][col] != B]
    
MATRIZ_TAREFA       = [[8, 3, B, 1, B, B, 6, B, 5],
                    [B, B, B, B, B, B, B, 8, B],
                    [B, B, B, 7, B, B, 9, B, B],
                    [B, 5, B, B, 1, 7, B, B, B],
                    [B, B, 3, B, B, B, 2, B, B],
                    [B, B, B, 3, 4, B, B, 1, B],
                    [B, B, 4, B, B, 8, B, B, B],
                    [B, 9, B, B, B, B, B, B, B],
                    [3, B, 2, B, B, 6, B, 4, 7]]

import copy
import random
class Tabuleiro:
    
    def __init__(self, matriz, fitness=0, preenchidos = None, calcPreenchidos=False):
        self.matriz = matriz
        self.fitness = fitness
        if calcPreenchidos:
            self.preenchidos = indicesPreenchidos(self.matriz)
        else:
            self.preenchidos = preenchidos
    
    def flip(self, lin, col):
        n = self.matriz[lin][col]
        n = (n+1)%9
        self.matriz[lin][col] = n
        
    def isNone(self,lin,col):
        return self.matriz[lin][col] is None
    
    def clone(self):
        return Tabuleiro(copy.deepcopy(self), \
                         preenchidos = self.preenchidos)
        
    def countInvalidos(self):
   
        count = 0
        for unidade in UNIDADES:
            valores = [self.matriz[pos[0]][pos[1]] for pos in unidade]
            for valor in valores:
                if valores.count(valor) > 1:
                    count += 1
        self.fitness = count
        return count
    
    def estahResolvido(self):
        '''
        :param tab: Tabuleiro
        :return: Boolean
        '''
        for lin in range(9):
            for col in range(9):
                if self.isNone(lin,col):
                    return False
        return True


    def preencheAleatorio(self):
        novoTab = self.clone()
        for lin in range(9):
            for col in range(9):
                if not (lin,col) in self.preenchidos:                   
                    novoTab[lin][col] = random.randrange(1,10)
        novoTab.countInvalidos()
        return novoTab
    
    def printthis(self):
        print_matriz(self.matriz)
    
    def __lt__(self,outro):
        return self.fitness < outro.fitness
    
    def __eq__(self, outro):
        # quando usar comparacao de igual, comparar pelo tab
        if isinstance(outro, Tabuleiro):
            return self.matriz == outro.matriz
        else:
            return outro == self
    
    def __getitem__(self,lin):
        return self.matriz[lin]
    
    def __len__(self):
        return len(self.matriz)
    
TAB_TAREFA = Tabuleiro(MATRIZ_TAREFA, calcPreenchidos=True)
print(TAB_TAREFA.preenchidos)             

