
# Jogador
# Created on 11 de Junho de 2021

from Jogador import Jogador
from Jogada import Jogada
from Tabuleiro import Tabuleiro
import time
import threading
import numpy as np
import copy

# Esta Classe implementa o esqueleto de um jogador guloso.
#
# Ele se conecta no servidor do jogo  no host passado pela linha de argumentos e
# na porta fornecida pela classe Servidor.
# Passa ent&atilde;o a receber as jogadas do oponente e enviar jogadas por meio do servidor
# segundo um protocolo pr&eacute;-definido.
#
# Execucao
# java Jogador <nome> <host>
# Exemplo:
# java Jogador equipe1 localhost
# <b>Protocolo</b>
# A cada rodada o jogador recebe uma jogada e envia uma jogada.
# A jogada recebida possui o seguinte formato:
# <jogador>\n<x>\n<y>\n<xp>\n<yp>\n
# Onde:
#
# <jogador>= indica qual &eacute; a cor do jogador (Tabuleiro.AZUL ou Tabuleiro.VERM) ou
# '#' indicando fim do jogo.
# <x><y> = sao as coordenadas da posicao recem ocupada (0 a 7).
# <xp><yp> = sao as coordenadas da pe&ccedil;a responsavel pela jogada (0 a 7).
#
# A jogada enviada possui o seguinte formato:
# <x>\n<y>\n<xp>\n<yp>\n
# Se o jogador precisar passar a jogada deve atribuir valor -1 as coordenadas.
#
# Caso o jogador tenha algum problema ou desista deve enviar o caracter #
#
# @author Alcione
# @version 1.0
class node():
    def __init__(self,tab,prof,pai,valor,jogador,jogada):
        self.jogada=jogada
        if prof%2==0:
            self.max=True
        else:
            self.max=False
        if jogador==Tabuleiro.AZUL:
            self.oponente=Tabuleiro.VERM
        else:
            self.oponente=Tabuleiro.AZUL
        self.jogador=jogador
        self.tab=copy.deepcopy(tab)
        self.prof=prof
        self.pai=pai
        self.valor=valor
class arvore():
    def __init__(self,prof,tab,jogador):
        self.jogador=jogador
        self.prof=prof
        self.tab=copy.deepcopy(tab)
        self.a=[node(tab,0,-1,None,jogador,None)]
        self.b=[]
        self.v1=np.asarray(self.a)
        self.folhas=np.asarray(self.b)
    def primeirai(self):
        i=0
        while True:
            if i==self.v1.size:
                break
            auxtab=copy.deepcopy(self.v1[i].tab)
            if self.v1[i].prof!=(self.prof-1):
                a=auxtab.obtemJogadasPossiveis(self.v1[i].jogador)
                for j in a:
                    auxtab1=copy.deepcopy(self.v1[i].tab)
                    auxtab1.move(self.v1[i].jogador,j)
                    self.v1=np.append(self.v1,node(auxtab1,self.v1[i].prof+1,i,None,self.v1[i].oponente,j))
            elif self.v1[i].prof==(self.prof-1):
                a=auxtab.obtemJogadasPossiveis(self.v1[i].jogador)
                for j in a:
                    auxtab1=copy.deepcopy(self.v1[i].tab)
                    auxtab1.move(self.v1[i].jogador,j)
                    self.folhas=np.append(self.folhas,node(auxtab1,self.v1[i].prof+1,i,None,self.v1[i].oponente,j))
            i+=1
        i=0
        while True:
            if i==self.folhas.size:
                break
            v=self.folhas[i].tab.heuristicaBasica(self.folhas[i].jogador,self.folhas[i].tab.tab)
            nodo=self.folhas[i]
            nodo.valor=v
            nodopai=self.v1[nodo.pai]
            while nodo.pai!=-1:
                nodopai=self.v1[nodo.pai]
                if nodopai.valor==None:
                    nodopai.valor=nodo.valor
                if nodopai.max:
                    if nodo.valor>nodopai.valor:
                        nodopai.valor=nodo.valor
                        if nodo.pai==0:
                            nodopai.jogada=nodo.jogada
                            print(nodo.jogada.linha,nodo.jogada.coluna)
                    else:
                        break
                else:
                    if nodo.valor<nodopai.valor:
                        nodopai.valor=nodo.valor
                    else:
                        break
                nodo=nodopai
            i+=1
        print("terminei")

    



class JogadorMinMax(Jogador):

    def __init__(self, nome):
        Jogador.__init__(self, nome)
        self.MAXNIVEL = 10
        self.TEMPOMAXIMO = 0.5
        self.jogada = Jogada(-1, -1, -1, -1)

     # Calcula uma nova jogada para o tabuleiro e jogador corrente.
     # Aqui deve ser colocado o algoritmo com as t&eacute;cnicas de inteligencia
     # artificial. No momento as jogadas s&atilde;o calculadas apenas por crit&eacute;rio de
     # validade. Coloque aqui seu algoritmo minmax.
     # @param tab Tabuleiro corrente
     # @param jogadorCor Jogador corrente
     # @return retorna a jogada calculada.

    def calculaJogada(self, tab, jogadorCor):
        tempo1 = time.time()
        usado = 0.0
        for prof in range(1, self.MAXNIVEL):
            tempo2 = time.time()
            if (tab.numPecas(0)+tab.numPecas(1))==0:
                self.jogada = Jogada(-1, -1, 0, 1)
            else:
                a=arvore(prof,tab,jogadorCor)
                t1 = threading.Thread(
                    target=a.primeirai())
                t1.start()
                t1.join(self.TEMPOMAXIMO - usado)
                usado = tempo2 - tempo1
                print("tempo usado:", usado)
                if a.v1[0].jogada != None :
                    self.jogada = a.v1[0].jogada
                usado = tempo2 - tempo1
                print("tempo usado:", usado)
                if usado >= self.TEMPOMAXIMO:
                    break

        return self.jogada



if __name__ == "__main__":
    import sys
    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")
