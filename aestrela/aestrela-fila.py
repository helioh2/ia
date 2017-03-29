#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from Queue import PriorityQueue

##Constantes:
B = None
VALORES = range(1,9)

DIR = (0,1)
ESQ = (0,-1)
BAIXO = (1,0)
CIMA = (-1,0)

DIRS = [DIR,ESQ,BAIXO,CIMA]


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

tab2 =  [[8,1,7],
         [3,B,5],
         [6,2,4]]
MANTAB2 = 4+3+2+3+2

tab3 = [[8,1,7],
         [3,4,5],
         [6,2,B]]
MANTAB3 = 4+3+3+4

# Valor é Int[1,8] ou B (None)

# Node
class Node:
    def __init__(self, tab, g, gh):
        self.tab = tab
        self.g = g
        self.gh = gh



contNodes = 0


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
    for lin in range(3):
        for col in range(3):
            atual = tab[lin][col]
            linOk, colOk = findN(tabOk,atual)
            #print(linOk, colOk)
            distancia = abs(linOk-lin) + abs(colOk-col)
            #print(distancia)
            soma += distancia
            
    return soma
            
def foraDoLugar(tab):
    soma = 0
    for lin in range(3):
        for col in range(3):
            atual = tab[lin][col] if tab[lin][col] != B else 0
            if atual != 3*lin + col:
                soma += 1
                #print(lin,col)
            
    return soma
                        
            
FRONTEIRA = []

def expandNode(x,h):
    proximos = [moveB(x.tab,direc) for direc in DIRS]
    proximos = [tab for tab in proximos if tab is not None]
    g = x.g + 1
    heuristicas = [h(tab) for tab in proximos]
    return [Node(tab,g,g+h) for tab,h in zip(proximos,heuristicas)]


def estahResolvido(tab):
    return tab == tabOk

import sys
sys.setrecursionlimit(10000)

def busca(tab,h):
    x = Node(tab,0,0+h(tab))
    # Node -> Node
    def buscaAux(x, h):    
                 
        fronteira = PriorityQueue()
        fronteira.put((x.gh,x))
        visitados = []
        expanded = 0
        
        while not fronteira.empty():
            
            gh, proximo = fronteira.get()
            if (estahResolvido(proximo.tab)):
                return proximo
            
            visitados.append(proximo.tab)
            
            descendentes = expandNode(proximo,h)
            descendentes = [d for d in descendentes if d.tab not in visitados]
            for d in descendentes:              
                fronteira.put((d.gh,d))
            print(fronteira.qsize())
            expanded += 1
            print(expanded)
            print(proximo.tab)
            

    return buscaAux(x,h)



import unittest

class Test(unittest.TestCase):

    def testFindB(self):
        self.assertEqual(findB(tab1),(0,0))
        self.assertEqual(findB(tab2),(1,1))
        self.assertEqual(findB(tab3),(2,2))

    def testMoves(self):
        self.assertEqual(moveBEsq(tab2),[[8,1,7],\
                                        [B,3,5],\
                                        [6,2,4]])
        self.assertEqual(moveBDir(tab2),[[8,1,7],\
                                [3,5,B],\
                                [6,2,4]])  
        self.assertEqual(moveBCima(tab2),[[8,B,7], \
                                   [3,1,5],\
                                   [6,2,4]])
        self.assertEqual(moveBBaixo(tab2),[[8,1,7], \
                                    [3,2,5],\
                                    [6,B,4]])

        self.assertEqual(moveBEsq(tab3),[[8,1,7], \
                                 [3,4,5],\
                                 [6,B,2]])
        self.assertEqual(moveBDir(tab3),None)
        self.assertEqual(moveBCima(tab3),[[8,1,7], \
                                     [3,4,B],\
                                     [6,2,5]])
        self.assertEqual( moveBBaixo(tab3),None)


        self.assertEqual( moveBEsq(tab1), None)
        self.assertEqual( moveBDir(tab1), [[1,B,7], \
                                [3,8,5],\
                                [6,2,4]])
        self.assertEqual( moveBCima(tab1),None)
        self.assertEqual( moveBBaixo(tab1), [[3,1,7], \
                                   [B,8,5],\
                                   [6,2,4]])

        self.assertEqual(moveB(tab2, (0,1)), [[8,1,7],\
                                [3,5,B],\
                                [6,2,4]]) 

    def testProximosFilhos(self):
        #self.assertEqual( proximos_filhos(tab1),[moveBEsq(tab1), moveBDir(tab1), moveBCima(tab1), moveBBaixo(tab1)] )
        pass

    def testManhattan(self):
        self.assertEqual(manhattan(tab1),MANTAB1)
        self.assertEqual(manhattan(tab2),MANTAB2)
        self.assertEqual(manhattan(tab3),MANTAB3)
        self.assertEqual(manhattan(tabOk),MANTABOK)

    def testForaDoLugar(self):
        self.assertEqual(foraDoLugar(tab1),4)
        self.assertEqual(foraDoLugar(tab2),5)
        self.assertEqual(foraDoLugar(tab3),4)
        self.assertEqual(foraDoLugar(tabOk),0)

    def testBusca(self):
        # self.assertEqual(busca(tabOk,foraDoLugar).tab,tabOk)
        # self.assertEqual(busca(tab1,foraDoLugar).tab,tabOk)
        #self.assertEqual(busca(tab2,foraDoLugar).tab,tabOk)
        # self.assertEqual(busca(tab3,foraDoLugar).tab,tabOk)

         #self.assertEqual(busca(tab1,manhattan).tab,tabOk)
         self.assertEqual(busca(tab2,manhattan).tab,tabOk)
         #self.assertEqual(busca(tab3,manhattan).tab,tabOk)

unittest.main()

#testes manuais:

#solucaoTab1h1 = busca(tab1,foraDoLugar)
#print(solucaoTab1h1)
