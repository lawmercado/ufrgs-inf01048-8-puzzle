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
    def custo(self, value):
        self.__custo = value
    
    def __str__(self):
        return "(%s, %s, %s, %d)" % (self.estado, self.pai.estado, self.acao, self.custo)
    
    def __lt__(self, other):
        return self._custo_prioridades() < other._custo_prioridades()

    def _custo_prioridades(self):
        return self._h() + self._g()   
    
    def _h(self):
        return self._distancia_hamming(self.estado)

    def _g(self):
        return self.custo
    
    def _distancia_hamming(self, inicial, objetivo="12345678_" ):
        """
        computa o número de peças fora do lugar, dado um estado inicial e final

        :param inicial: str
        :param objetivo: str, optional
        :return:
        """

        count = 0
        for index, value in enumerate(objetivo):
            if inicial[index] != objetivo[index]:
                count += 1

        return count

class FilaPrioridade:
    """
    classe que encapsula métodos do módulo python heapq - Heap queue algorithm: 
    https://docs.python.org/3/library/heapq.html

    """
    def __init__(self):
        self.fila = []

    def push(self, item):
        heappush(self.fila, item)
    
    def pop(self):
        return heappop(self.fila)
    
    def __len__(self):
        return len(self.fila)


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


def astar_hamming(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    """

    def retira(fronteira): # TODO: Usar typehinting na classe customizada FilaPrioridade
        v = fronteira.pop()

        return v, fronteira

    return _busca_grafo_prioridades(estado, retira)


def astar_manhattan(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None.

    :param estado: str
    :return:
    
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


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
    

def _busca_grafo_prioridades(estado_incial: str, retira,
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
    fronteira = FilaPrioridade()
    fronteira.push(Nodo(estado_incial, None, None, 0))

    while len(fronteira) > 0:
        v, fronteira = retira(fronteira)

        if v.estado == estado_objetivo:
            return _obter_caminho(v)

        if v.estado not in explorados:
            explorados.add(v.estado)
            expande_nodos = expande(v)
            for value in expande_nodos:
                value.custo = len(fronteira)
                fronteira.push(value)

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

def _distancia_manhattan(estado: str, estado_objetivo="12345678_"):
    manhattan_distance = 0
    obj_array = _string_para_array(estado_objetivo)
    current = _string_para_array(estado)

    for i in range(3):
        for j in range(3):
            if current[i][j] != '_' and current[i][j] != obj_array[i][j]:
                print("fora do lugar!", current[i][j])
                index = np.where(obj_array == current[i][j])
                # TODO
                # manhattan_distance += abs(i - index_x) + abs(j - index_y)

    return manhattan_distance
