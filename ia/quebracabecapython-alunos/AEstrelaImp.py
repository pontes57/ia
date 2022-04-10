import heapq
from Posicao import Posicao
from AEstrela import AEstrela
from QuebraCabeca import QuebraCabeca
from QuebraCabecaImp import QuebraCabecaImp
import copy

class st:
    def __init__(self,nivel,valor,jogo,ph,posicao):#struct que guarda em qual iteracao estou,o valor do meu estado,o meu estado,o hash do meu pai e qual movimento fiz
        self.nivel=nivel
        self.valor=valor
        self.jogo=jogo
        self.ph=ph
        self.posicao=posicao

class AEstrelaImp(AEstrela):
    fila=[]#fila de prioridade onde vou pegar os menores valores
    disc={}#discionario que guarda os estados dos jogos
    def init(self):
        a = 3
    def possible(qc):#funcao pra saber se o jogo e' possivel
        tab=qc.getTab()
        inversoes = 0
        for i in range(0, 3) :
            for j in range(0, 3) :
                for l in range(i, 3) :
                    for k in range(0, 3) :
                        if (tab[i][j] > -1 and tab[l][k] > -1 and tab[i][j] > tab[l][k]) :
                            if(i==l and k<=j):
                                continue
                            inversoes += 1
        return (inversoes % 2 != 0)

    def loop ():#funcao que pega o menor valor da fila e expande seus filhos ate achar a resposta
        while(AEstrelaImp.fila):
            h=heapq.heappop(AEstrelaImp.fila)[1]#pego o hashcode
            nodo=AEstrelaImp.disc[h]#pego o struct
            vazio=nodo.jogo.getPosVazio()
            possibilidades=nodo.jogo.getMovePossiveis()
            for movimento in possibilidades:#para cada possivel movimento
                proximo_jogo = copy.deepcopy(nodo.jogo)#faco uma copia para poder modificar sem interferir no pai
                
                proximo_jogo.move(vazio.getLinha(), vazio.getColuna(), movimento.getLinha(), movimento.getColuna())
                if (proximo_jogo.isOrdenado()):
                    return st(nodo.nivel+1,proximo_jogo.getValor(),proximo_jogo,nodo.jogo.hashCode(),proximo_jogo.getPosVazio())#retorno o struct com as infomacoes da solucao
                if(proximo_jogo.hashCode() not in AEstrelaImp.disc):#para nao repetir jogos
                    heapq.heappush(AEstrelaImp.fila, (nodo.nivel+1 + proximo_jogo.getValor(), proximo_jogo.hashCode()))
                    AEstrelaImp.disc[proximo_jogo.hashCode()]=st(nodo.nivel+1,proximo_jogo.getValor(),proximo_jogo,nodo.jogo.hashCode(),proximo_jogo.getPosVazio())

    def getSolucao( self , qc ):
        if(qc.isOrdenado()):
            return[]
        if(AEstrelaImp.possible(qc)):
            print("not solvable")
            return[]
        hash=qc.hashCode()
        valor=qc.getValor()
        primeiro=st(0,valor,qc,None,None)#primeiro estado do jogo
        AEstrelaImp.disc[hash]=primeiro
        AEstrelaImp.fila.append((valor,hash))
        resultado=AEstrelaImp.loop()#pego a resposta
        ordem=[resultado.posicao]#vetor com os movimentos que ira ser retornado
        nodo=AEstrelaImp.disc[resultado.ph]
        while (nodo.nivel!=0):
            ordem.append(nodo.posicao)
            nodo=AEstrelaImp.disc[nodo.ph]
        ordem.reverse()
        return ordem


