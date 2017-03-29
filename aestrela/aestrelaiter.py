#!/usr/bin/env python
# -*- coding: utf-8 -*-


import copy
import bisect

##Constantes:
B = None
VALORES = range(1,9)

DIR = (0,1)
ESQ = (0,-1)
BAIXO = (1,0)
CIMA = (-1,0)

DIRS = [DIR,ESQ,BAIXO,CIMA]
DIRNOMES = ["DIR","ESQ","BAIXO","CIMA"]


##Definições dos dados:

# Tab é matriz 3x3 com Valor

tabOk = [[B,1,2],
         [3,4,5],
         [6,7,8]]
MANTABOK = 0
tab1 =  [[B,1,7],
         [3,8,5],
         [6,2,4]]
MANTAB1 = 3+2+3+2

tab2 =  [[1,8,7],
         [3,B,5],
         [4,6,2]]
MANTAB2 = 1+3+3+2+2+1+2

tab3 = [[8,1,7],
         [3,4,5],
         [6,2,B]]
MANTAB3 = 4+3+3+4

# Valor é Int[1,8] ou B (None)

# Node
class Node:
    def __init__(self, tab, g, gh, pai = None, move = None):
        self.tab = tab
        self.g = g
        self.gh = gh
        self.pai = pai
        self.move = move
        
    def __lt__(self, outro):
        #compara qual o menor pelo gh
        return self.gh < outro.gh

    def __eq__(self, outro):
        # quando usar comparacao de igual, comparar pelo tab
        if isinstance(outro, Node):
            return self.tab == outro.tab
        else:
            return outro == self
        
    def expandNode(self,h):
        proximos = [moveB(self.tab,direc) for direc in DIRS]
    #     proximos = [tab for tab in proximos if tab is not None]
        g = self.g + 1
        heuristicas = [h(tab) for tab in proximos]
        return [Node(tab,g,g+h,self,d) for tab,h,d in \
                zip(proximos,heuristicas,DIRS) \
                if tab is not None]
  

def findN(tab,n):
    for lin in range(3):
        for col in range(3):
            if tab[lin][col] == n:
                return (lin,col)

def findB(tab):
    return findN(tab,B)

def moveB(tab,direc):
    posB = linB, colB = findB(tab)
    linMove, colMove = tuple(map(lambda x, y: x + y, posB, direc))
    if linMove not in range(0,3) or colMove not in range(0,3):
        return None
    tabNovo = copy.deepcopy(tab)
    tabNovo[linMove][colMove], tabNovo[linB][colB] = B, tab[linMove][colMove]
    return tabNovo

def moveBEsq(tab):
    return moveB(tab,ESQ)

def moveBDir(tab):
    return moveB(tab,DIR)

def moveBCima(tab):
    return moveB(tab,CIMA)

def moveBBaixo(tab):
    return moveB(tab,BAIXO)


def manhattan(tab):
    soma = 0
    if not tab:
        return None
    for lin in range(3):
        for col in range(3):
            atual = tab[lin][col] if tab[lin][col] != B else 0
            linOk, colOk = atual//3, atual%3
            distancia = abs(linOk-lin) + abs(colOk-col)
            soma += distancia
            
    return soma
            
def hamming(tab):
    soma = 0
    if not tab:
        return None
    for lin in range(3):
        for col in range(3):
            atual = tab[lin][col] if tab[lin][col] != B else 0
            if atual != 3*lin + col:
                soma += 1
                #print(lin,col)
            
    return soma



def estahResolvido(tab):
    return tab == tabOk


def busca(tab,h):
    x = Node(tab,0,0)
    # Node -> Node
    def buscaAux(x, h):     
        fronteira = [x]
        visitados = []
        while fronteira:
            
            proximo = fronteira.pop(0)
            if (estahResolvido(proximo.tab)):
                return proximo
                
            visitados.append(proximo)
            
            descendentes = proximo.expandNode(h)
            for d in descendentes:
                if d not in fronteira and d not in visitados:
                    bisect.insort(fronteira, d)
            print(len(visitados))
#             print("\n\n\n\n")
#             for node in fronteira:
                
            print(fronteira[0].g,fronteira[0].gh, fronteira[0].gh - fronteira[0].g)

    return buscaAux(x,h)

def extrairMoves(x):
    moves = []
    while x:
        moves.append(x.move)
        x = x.pai
    moves.reverse()
    return moves

def traduzirMoves(moves):
    movesTrad = []
    for m in moves:
        if not m: continue
        nome = DIRNOMES[DIRS.index(m)]
        movesTrad.append(nome)
    return movesTrad


#testes manuais:

#solucaoTab1h1 = busca(tab1,hamming)
#print(solucaoTab1h1)

resbuscatab1 = busca(tab2,manhattan)
print(resbuscatab1.move)
print(extrairMoves(resbuscatab1))
print(traduzirMoves(extrairMoves(resbuscatab1)))
