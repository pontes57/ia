
# Jogador
# Created on 11 de Junho de 2021

from Tabuleiro import Tabuleiro
from jogadorbaseG3 import JogadorbaseG3
from Jogada import Jogada
from TabuleiroG3 import TabuleiroG3
import time
import threading
import numpy as np
import copy#classe usada pra copiar objetos

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
global acabou#variavel global pra thread saber que deve parar
acabou=False
class node():#classe que representa um nodo da arvore
    def __init__(self,tab,prof,pai,valor,jogador,jogada):#recebe o tabuleiro,profundidade,posicao do pai no vetor,o valor heuristico,de quem eh a vez de jogar,e a jogada feita pra chegar\e ali
        self.alfabeta=True #variavel pra saber se devo executar o corte alfabeta
        self.jogada=jogada
        if prof%2==0:
            self.max=True #descobre se eh um nodo max ou min
        else:
            self.max=False
        if jogador==TabuleiroG3.AZUL:
            self.oponente=TabuleiroG3.VERM#descobre o inimigo
        else:
            self.oponente=TabuleiroG3.AZUL
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
        self.a=[node(tab,0,-1,None,jogador,None)]#cria o vetor com o primeiro nodo da arvore
        self.b=[]
        self.v1=np.asarray(self.a)#vetor onde vai estar os nodos que nao sao folhas
        self.folhas=np.asarray(self.b)#vetor vai estar os nodos folhas,comeca vazio
    def primeirai(self):#primeira iteracao que vai gerar os nodos da arvore
        i=0
        while True:
            if i==self.v1.size:#enquanto ele nao gerou todos os filhos de cada nodo no vetor v1
                break
            auxtab=copy.deepcopy(self.v1[i].tab)
            if self.v1[i].prof!=(self.prof-1):#enquanto nao eh o penultimo nivel
                a=auxtab.obtemJogadasPossiveis(self.v1[i].jogador)#pega todas as jogadas possiveis
                for j in a:#pra cada jogada possivel
                    auxtab1=copy.deepcopy(self.v1[i].tab)
                    auxtab1.move(self.v1[i].jogador,j)#faz o movimento
                    self.v1=np.append(self.v1,node(auxtab1,self.v1[i].prof+1,i,None,self.v1[i].oponente,j))
            elif self.v1[i].prof==(self.prof-1):#caso seja o penultimo nivel os seus filhos serao as folhas
                a=auxtab.obtemJogadasPossiveis(self.v1[i].jogador)
                for j in a:
                    auxtab1=copy.deepcopy(self.v1[i].tab)
                    auxtab1.move(self.v1[i].jogador,j)
                    self.folhas=np.append(self.folhas,node(auxtab1,self.v1[i].prof+1,i,None,self.v1[i].oponente,j))
            i+=1
            global acabou
            if acabou:
                return
        self.segundai()

    def segundai(self):#segunda iteracao onde vamos pegar a heuristica de cada folha e chamar a funcao que ira fazer a atualizacao dos pais
        i=0
        while True:
            if i==self.folhas.size:#enquanto nao pegamos o valor de cada folha
                break
            v=self.folhas[i].tab.heuristicaBasica(self.jogador,self.folhas[i].tab.tab)#pega o valor heuristico de cada folha
            nodo=self.folhas[i]
            nodo.valor=v
            self.recursiva(nodo)
            i+=1
            global acabou
            if acabou:
                return

    def recursiva(self,nodo):#funcao que pega o valor heuristico de cada nodo e vai atualizando os pais dele
        nodopai=self.v1[nodo.pai]
        if nodopai.alfabeta==False:#caso o nodo pai ja tenha sido cortado no corte alfabeta
            return False#retorno dizendo que realizei o corte alfabeta
        else:
            if nodopai.valor==None:#caso meu pai ainda n tenha algum valor
                nodopai.valor=nodo.valor#atualizo o valor heuristico do meu pai
                if nodo.pai==0:#caso seja a raiz digo pra ela qual a jogada a ser feita
                        nodopai.jogada=nodo.jogada
                        return True#retorno dizendo que nao realizei o corte alfabeta
            if nodopai.max:#caso meu pai seja max vejo se meu valor é maior
                if nodo.valor>nodopai.valor:
                    nodopai.valor=nodo.valor#atualizo o valor heuristico do meu pai
                    if nodo.pai==0:#caso seja a raiz digo pra ela qual a jogada a ser feita
                        nodopai.jogada=nodo.jogada
                        return True#retorno dizendo que nao realizei o corte alfabeta
                else:
                    nodo.alfabeta=False
                    return False#retorno dizendo que realizei o corte alfabeta
            else:
                if nodo.valor<nodopai.valor:#caso meu pai seja min vejo se meu valor é menor
                    nodopai.valor=nodo.valor
                else:
                    nodo.alfabeta=False
                    return False#retorno dizendo que realizei o corte alfabeta
        retorno=self.recursiva(nodopai)
        nodo.alfabeta=retorno#irei realizar o corte se algum dos meus pais foram cortados
        return retorno




class JogadorMinMax(JogadorbaseG3):

    def __init__(self, nome):
        JogadorbaseG3.__init__(self, nome)
        self.MAXNIVEL = 10
        self.TEMPOMAXIMO = 4.92
        self.jogada = Jogada(-1, -1, -1, -1)
        self.valor=-1000000#valor da jogada heuristica selecionada

     # Calcula uma nova jogada para o tabuleiro e jogador corrente.
     # Aqui deve ser colocado o algoritmo com as t&eacute;cnicas de inteligencia
     # artificial. No momento as jogadas s&atilde;o calculadas apenas por crit&eacute;rio de
     # validade. Coloque aqui seu algoritmo minmax.
     # @param tab Tabuleiro corrente
     # @param jogadorCor Jogador corrente
     # @return retorna a jogada calculada.

    def calculaJogada(self, tab, jogadorCor):
        global acabou
        acabou=False
        tempo1 = time.time()
        usado = 0.0
        for prof in range(1, self.MAXNIVEL):
            tempo2 = time.time()
            usado = tempo2 - tempo1
            a=arvore(prof,tab,jogadorCor)#crio a arvore
            t1 = threading.Thread(
                target=self.max, args=(tab, jogadorCor, prof,a))
            t1.start()
            t1.join(self.TEMPOMAXIMO - usado)
            tempo2 = time.time()
            if (a.v1[0].jogada != None and a.v1[0].valor>self.valor):#caso essa iteracao ja tenha gerada uma jogada e ela é melhor que a atual pego ela
                self.jogada = a.v1[0].jogada
                self.valor=a.v1[0].valor
            usado = tempo2 - tempo1
            print("tempo usado:", usado)
            if usado >= self.TEMPOMAXIMO:
                break
        acabou=True#flag pras threads saberem que o programa ja acabou
        self.valor=-1000000
        return self.jogada

    def max(self, tab, jogador, prof,a):
        a.primeirai()


if __name__ == "__main__":
    import sys
    JogadorMinMax(sys.argv[1]).joga()
    print("Fim")
