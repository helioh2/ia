'''
Created on 28 de mar de 2017

@author: helio
'''
import unittest

from aestrela.aestrelaiter import *

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

    def testhamming(self):
        self.assertEqual(hamming(tab1),4)
        self.assertEqual(hamming(tab2),7)
        self.assertEqual(hamming(tab3),4)
        self.assertEqual(hamming(tabOk),0)

    def testBusca(self):
        self.assertEqual(busca(tabOk,hamming).tab,tabOk)
        self.assertEqual(busca(tab1,hamming).tab,tabOk)
        self.assertEqual(busca(tab2,hamming).tab,tabOk)
        self.assertEqual(busca(tab3,hamming).tab,tabOk)
        self.assertEqual(busca(tab1,manhattan).tab,tabOk)
        self.assertEqual(busca(tab2,manhattan).tab,tabOk)
        self.assertEqual(busca(tab3,manhattan).tab,tabOk)

 
unittest.main()