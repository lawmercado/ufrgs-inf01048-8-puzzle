from typing import List, Tuple
import numpy as np


class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado: str, pai, acao: str, custo: int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
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

    def __str__(self):
        return "(%s, %s, %s, %d)" % (self.estado, self.pai.estado, self.acao, self.custo)


def __string_para_array(estado: str) -> np.ndarray:
    return np.array(list(estado), dtype=str).reshape((3, 3))


def __array_para_string(estado: np.ndarray) -> str:
    return "".join(estado.ravel())


def sucessor(estado: str) -> List[Tuple[str, str]]:
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """

    estados = []

    estado = __string_para_array(estado)

    posicao_espaco = np.where(estado == "_")
    i, j = posicao_espaco[0].item(), posicao_espaco[1].item()

    if i > 0:  # i.e. Se não está na linha mais acima
        estado_acima = estado.copy()
        estado_acima[i][j] = estado_acima[i - 1][j]
        estado_acima[i - 1][j] = "_"

        estados.append(("acima", __array_para_string(estado_acima)))

    if i < 2:  # i.e. Se não está na linha mais abaixo
        estado_abaixo = estado.copy()
        estado_abaixo[i][j] = estado_abaixo[i + 1][j]
        estado_abaixo[i + 1][j] = "_"

        estados.append(("abaixo", __array_para_string(estado_abaixo)))

    if j < 2:  # i.e. Se não está na coluna mais a direita
        estado_direita = estado.copy()
        estado_direita[i][j] = estado_direita[i][j + 1]
        estado_direita[i][j + 1] = "_"

        estados.append(("direita", __array_para_string(estado_direita)))

    if j > 0:  # i.e. # i.e. Se não está na coluna mais a esquerda
        estado_esquerda = estado.copy()
        estado_esquerda[i][j] = estado_esquerda[i][j - 1]
        estado_esquerda[i][j - 1] = "_"

        estados.append(("esquerda", __array_para_string(estado_esquerda)))

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
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def dfs(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_hamming(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado: str) -> List[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
