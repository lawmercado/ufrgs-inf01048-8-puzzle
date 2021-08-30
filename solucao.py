import itertools
from collections import deque
from heapq import heappop, heappush
from typing import Callable, Deque, List, Tuple

import numpy as np


class Nodo:
    def __init__(self, estado: str, pai, acao: str, custo: int):
        """
        Inicializa o nodo com os atributos recebidos.

        :param estado: str, representacao do estado do 8-puzzle
        :param pai: Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao: str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo: int, custo do caminho da raiz até este nó
        """

        self.__estado = estado
        self.__pai = pai
        self.__acao = acao
        self.__custo = custo

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def pai(self):
        return self.__pai

    @property
    def acao(self) -> str:
        return self.__acao

    @property
    def custo(self) -> int:
        return self.__custo

    @custo.setter
    def custo(self, valor):
        self.__custo = valor
    
    def __str__(self):
        return "Nodo (estado: %s, pai: %s, acao: %s, custo: %d)" %\
               (self.estado,
                self.pai.estado if self.pai else "<raiz>",
                self.acao if self.acao else "<raiz>",
                self.custo)


class FilaPrioridade:
    """
    Encapsula métodos do módulo python heapq - Heap queue algorithm:
    https://docs.python.org/3/library/heapq.html

    """
    def __init__(self, prioridade: Callable[[Nodo], int]):
        self._fila = []
        self._prioridade = prioridade
        self._contador = itertools.count()

    def push(self, nodo: Nodo):
        """
        Adiciona um nodo ao heap. Para decidir a prioridade, uma função é informada.
        Além disso, para critério de desempate é usado um contador, conforme sugerido na documentação.

        :param nodo: Nodo
        :return:
        """
        heappush(self._fila, (self._prioridade(nodo), next(self._contador), nodo))
    
    def pop(self) -> Nodo:
        return heappop(self._fila)[-1]
    
    def __len__(self):
        return len(self._fila)


def sucessor(estado: str) -> List[Tuple[str, str]]:
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.

    :param estado: str
    :return:
    """

    estados = []

    estado = _string_para_array(estado)

    posicao_espaco = np.where(estado == "_")
    i, j = posicao_espaco[0].item(), posicao_espaco[1].item()

    if i > 0:  # i.e. Se não está na linha mais acima
        estado_acima = estado.copy()
        estado_acima[i][j] = estado_acima[i - 1][j]
        estado_acima[i - 1][j] = "_"

        estados.append(("acima", _array_para_string(estado_acima)))

    if i < 2:  # i.e. Se não está na linha mais abaixo
        estado_abaixo = estado.copy()
        estado_abaixo[i][j] = estado_abaixo[i + 1][j]
        estado_abaixo[i + 1][j] = "_"

        estados.append(("abaixo", _array_para_string(estado_abaixo)))

    if j < 2:  # i.e. Se não está na coluna mais a direita
        estado_direita = estado.copy()
        estado_direita[i][j] = estado_direita[i][j + 1]
        estado_direita[i][j + 1] = "_"

        estados.append(("direita", _array_para_string(estado_direita)))

    if j > 0:  # i.e. # i.e. Se não está na coluna mais a esquerda
        estado_esquerda = estado.copy()
        estado_esquerda[i][j] = estado_esquerda[i][j - 1]
        estado_esquerda[i][j - 1] = "_"

        estados.append(("esquerda", _array_para_string(estado_esquerda)))

    return estados


def expande(nodo: Nodo) -> List[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.

    :param nodo: objeto da classe Nodo
    :return:
    """

    filhos = []

    for acao, estado in sucessor(nodo.estado):
        filhos.append(Nodo(estado, nodo, acao, nodo.custo + 1))

    return filhos


def bfs(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    """

    def retira(fronteira: Deque[Nodo]) -> Tuple[Nodo, Deque[Nodo]]:
        v = fronteira.popleft()

        return v, fronteira

    return _busca_grafo(estado, retira)


def dfs(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    """

    def retira(fronteira: Deque[Nodo]) -> Tuple[Nodo, Deque[Nodo]]:
        v = fronteira.pop()

        return v, fronteira

    return _busca_grafo(estado, retira)


def distancia_hamming(estado: str, estado_objetivo: str = "12345678_") -> int:
    distancia = 0

    for i in range(len(estado_objetivo)):
        if estado[i] != estado_objetivo[i]:
            distancia += 1

    return distancia


def astar_hamming(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    """

    def retira(fronteira: FilaPrioridade) -> Tuple[Nodo, FilaPrioridade]:
        v = fronteira.pop()

        return v, fronteira

    def prioridade(nodo: Nodo) -> int:
        return nodo.custo + distancia_hamming(nodo.estado)

    return _busca_grafo_prioridades(estado, retira, prioridade)


def distancia_manhattan(estado: str, estado_objetivo="12345678_") -> int:
    distancia = 0

    for i_estado, i_estado_objetivo in ((estado.index(str(i)), estado_objetivo.index(str(i))) for i in range(1, 9)):
        distancia += abs(i_estado % 3 - i_estado_objetivo % 3) + abs(i_estado // 3 - i_estado_objetivo // 3)

    return distancia


def astar_manhattan(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    
    """

    def retira(fronteira: FilaPrioridade) -> Tuple[Nodo, FilaPrioridade]:
        v = fronteira.pop()

        return v, fronteira

    def prioridade(nodo: Nodo) -> int:
        return nodo.custo + distancia_manhattan(nodo.estado)

    return _busca_grafo_prioridades(estado, retira, prioridade)


def executa_caminho(estado_inicial: str, caminho: List[str]) -> str or None:
    """
    Dado um estado inicial e um caminho (i.e. ações a serem executadas),
    retorna o estado em que esse conjunto de ações leva.
    Retorna None se o estado atingido é igual ao estado_inicial.

    :param estado_inicial: str
    :param caminho: list
    :return:
    """
    nodo = Nodo(estado_inicial, None, None, 0)

    if caminho is None:
        return None

    while len(caminho) > 0:
        filhos = expande(nodo)
        acao = caminho.pop(0)

        for filho in filhos:
            if filho.acao == acao:
                nodo = filho

                break

    return nodo.estado
    

def _busca_grafo_prioridades(estado_incial: str, retira: Callable[[FilaPrioridade], Tuple[Nodo, FilaPrioridade]],
                             prioridade: Callable[[Nodo], int], estado_objetivo="12345678_") -> List[str] or None:
    """
    Busca num grafo o estado_final partindo do estado_inicial, usando a função retira para remover
    itens da fronteira. Retorna o caminho do estado_inicial até o estado_final se este existir;
    None caso o contrário.

    :param estado_incial: str
    :param retira: callable, função que remove um item da fronteira
    :param estado_objetivo: str, optional
    :return:
    """

    explorados = set()  # Ordem não importa
    fronteira = FilaPrioridade(prioridade=prioridade)
    fronteira.push(Nodo(estado_incial, None, None, 0))

    while len(fronteira) > 0:
        v, fronteira = retira(fronteira)

        if v.estado == estado_objetivo:
            return _obter_caminho(v)

        if v.estado not in explorados:
            explorados.add(v.estado)

            for nodo in expande(v):
                nodo.custo = len(fronteira)
                fronteira.push(nodo)

    return None


def _busca_grafo(estado_incial: str, retira: Callable[[Deque[Nodo]], Tuple[Nodo, Deque[Nodo]]],
                 estado_objetivo="12345678_") -> List[str] or None:
    """
    Busca num grafo o estado_final partindo do estado_inicial, usando a função retira para remover
    itens da fronteira. Retorna o caminho do estado_inicial até o estado_final se este existir;
    None caso o contrário.

    :param estado_incial: str
    :param retira: callable, função que remove um item da fronteira
    :param estado_objetivo: str, optional
    :return:
    """

    explorados = set()  # Ordem não importa
    fronteira = deque()
    fronteira.append(Nodo(estado_incial, None, None, 0))

    while len(fronteira) > 0:
        v, fronteira = retira(fronteira)

        if v.estado == estado_objetivo:
            return _obter_caminho(v)

        if v.estado not in explorados:
            explorados.add(v.estado)
            fronteira.extend(expande(v))

    return None


def _string_para_array(estado: str) -> np.ndarray:
    return np.array(list(estado), dtype=str).reshape((3, 3))


def _array_para_string(estado: np.ndarray) -> str:
    return "".join(estado.ravel())


def _obter_caminho(nodo: Nodo) -> List[str]:
    """
    Dado um nodo, retorna o conjunto de ações que levam a esse nodo.

    :param nodo: objeto da classe Nodo
    :return:
    """
    caminho = []

    while nodo.pai is not None:
        caminho.append(nodo.acao)
        nodo = nodo.pai

    caminho.reverse()

    return caminho