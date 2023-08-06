"""
The abstraction that exists above Cell and Agent, and exists to store things in
common between the two
"""


class ElementTemplate:
    # {{{
    """
    Class that exists just to contain both AgentTemplate and CellTemplate, so
    agents and cells can share variables.
    """

    _agent_spawn_queue = []

    def spawn_agent(self, agent_tuple):
        # {{{
        ElementTemplate._agent_spawn_queue.append(agent_tuple)

    # }}}

    def __init__(self, val, pos, cell_args=None):
        # {{{
        self.lin, self.col = pos
        self.value = val

    # }}}

    def update(self, state_matrix, state_list=None):
        # {{{
        ...

    # }}}

    @classmethod
    def simulation_start(cls, state_matrix, state_list=None, cell_args=None):
        # {{{
        ...

    # }}}

    @classmethod
    def generation_start(cls, state_matrix, state_list=None):
        # {{{
        """
        Método executado somente uma vez no começo de cada geração. Por padrão não faz
        nada.
        """
        ...

    # }}}

    @classmethod
    def generation_end(cls, state_matrix, state_list=None):
        # {{{
        ...

    # }}}

    @property
    def pos(self):
        return (self.lin, self.col)

    @property
    def neighbors(self):
        # {{{
        raise NotImplementedError("Implemented in derived class")

    # }}}

    @property
    def moore_neighborhood(self):
        # {{{
        """
        Vizinhança de Moore. Retorna um array de numpy com 8
        elementos; a ordem é da esquerda para direita, de cima
        para baixo.
        """
        # pylint: disable=no-member

        # Provavelmente há uma maneira mais elegante de fazer
        # isso, mas essa é de longe a mais rápida e eficiente
        # que encontrei
        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        prev_lin, next_lin = lin - 1, lin + 1
        prev_col, next_col = col - 1, col + 1
        try:
            # Primeiro tenta acessar os elementos normalmente
            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[next_lin, prev_col],
                state_matrix[lin, prev_col],
            ]
        except IndexError:
            # Isso vai falhar para células nas beiradas da
            # matriz. Neste caso, acessa-se os elementos fazendo
            # o 'wrapping' ao redor da matriz.
            prev_lin %= m
            next_lin %= m
            prev_col %= n
            next_col %= n

            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[next_lin, prev_col],
                state_matrix[lin, prev_col],
            ]

        return neighbors

    # }}}

    @property
    def neumann_neighborhood(self):
        # {{{
        """
        Vizinhança de Von Neumann. Retorna um array numpy com 4
        elementos, começando com o de cima no sentido horário.
        """
        # pylint: disable=no-member

        # Sim, esse código é quase todo copiado e colado da
        # moore_neighborhood. Fazer o que? Isso precisa ser
        # rápido.
        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        prev_lin, next_lin = lin - 1, lin + 1
        prev_col, next_col = col - 1, col + 1
        try:
            # Primeiro tenta acessar os elementos normalmente
            neighbors = [
                state_matrix[prev_lin, col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[lin, prev_col],
            ]
        except IndexError:
            # Isso vai falhar para células nas beiradas da
            # matriz. Neste caso, acessa-se os elementos fazendo
            # o 'wrapping' ao redor da matriz.
            prev_lin %= m
            next_lin %= m
            prev_col %= n
            next_col %= n

            neighbors = [
                state_matrix[prev_lin, col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[lin, prev_col],
            ]
        return neighbors

    # }}}

    @property
    def triangular_edges_neighborhood(self):
        # {{{
        """
        Vizinhança triangular de arestas. Os vizinhos são, para células ímpares,
        respectivamente, as células da esquerda, cima e direita, e para células pares,
        as da esquerda, de baixo e da direita.
        """
        # pylint: disable=no-member

        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        parity = -1 if (lin + col) & 1 else 1
        parity_lin = lin + parity
        prev_col, next_col = col - 1, col + 1
        try:
            neighbors = [
                state_matrix[lin, prev_col],
                state_matrix[parity_lin, col],
                state_matrix[lin, next_col],
            ]
        except IndexError:
            parity_lin %= m
            prev_col %= n
            next_col %= n

            neighbors = [
                state_matrix[lin, prev_col],
                state_matrix[parity_lin, col],
                state_matrix[lin, next_col],
            ]
        return neighbors

    # }}}

    @property
    def triangular_vertices_neighborhood(self):
        # {{{
        """
        Vizinhança triangular de vértices. Retorna as 12 células que, num ladrilhamento
        triangular, compartilham ao menos 1 vértice com a célula. Células pares tem suas
        vizinhanças apontando 'para cima', e ímpares tem suas vizinhanças apontando
        'para baixo'.
        """
        # pylint: disable=no-member

        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        parity = -1 if (lin + col) & 1 else 1
        parity_lin = parity + lin
        prev_lin, next_lin = lin - 1, lin + 1
        prev_col, next_col = col - 1, col + 1
        prev_2col, next_2col = col - 2, col + 2
        try:
            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[next_lin, prev_col],
                state_matrix[lin, prev_col],
                state_matrix[lin, prev_2col],
                state_matrix[lin, next_2col],
                state_matrix[parity_lin, next_2col],
                state_matrix[parity_lin, prev_2col],
            ]
        except IndexError:
            parity_lin %= m
            next_lin %= m
            prev_lin %= m
            prev_col %= n
            next_col %= n
            next_2col %= n
            prev_2col %= n

            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[next_lin, prev_col],
                state_matrix[lin, prev_col],
                state_matrix[lin, prev_2col],
                state_matrix[lin, next_2col],
                state_matrix[parity_lin, next_2col],
                state_matrix[parity_lin, prev_2col],
            ]
        return neighbors

    # }}}

    @property
    def triangular_1vertex_neighborhood(self):
        # {{{
        """
        Vizinhança triangular de vértices. Retorna as 9 células que, num ladrilhamento
        triangular, compartilham somente 1 vértice com a célula. Células pares tem suas
        vizinhanças apontando 'para cima', e ímpares tem suas vizinhanças apontando
        'para baixo'.
        """
        # pylint: disable=no-member, too-many-locals

        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        parity = -1 if (lin + col) & 1 else 1
        parity_lin = parity + lin
        rev_parity_lin = -parity + lin
        prev_lin, next_lin = lin - 1, lin + 1
        prev_col, next_col = col - 1, col + 1
        prev_2col, next_2col = col - 2, col + 2
        try:
            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, prev_2col],
                state_matrix[lin, next_2col],
                state_matrix[next_lin, prev_col],
                state_matrix[next_lin, next_col],
                state_matrix[parity_lin, prev_2col],
                state_matrix[parity_lin, next_2col],
                state_matrix[rev_parity_lin, col],
            ]
        except IndexError:
            parity_lin %= m
            next_lin %= m
            prev_lin %= m
            prev_col %= n
            next_col %= n
            next_2col %= n
            prev_2col %= n
            rev_parity_lin %= m

            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, next_col],
                state_matrix[lin, prev_2col],
                state_matrix[lin, next_2col],
                state_matrix[next_lin, prev_col],
                state_matrix[next_lin, next_col],
                state_matrix[parity_lin, prev_2col],
                state_matrix[parity_lin, next_2col],
                state_matrix[rev_parity_lin, col],
            ]
        return neighbors

    # }}}

    @property
    def hexagonal_neighborhood(self):
        # {{{
        """
        Vizinhança hexagonal. Semelhante à de Moore mas não conta os vizinhos do canto
        superior direito e inferior esquerdo.
        """
        # pylint: disable=no-member

        state_matrix = self.state_matrix
        m, n = state_matrix.shape
        lin, col = self.lin, self.col
        prev_lin, next_lin = lin - 1, lin + 1
        prev_col, next_col = col - 1, col + 1
        try:
            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[lin, prev_col],
            ]
        except IndexError:
            prev_lin %= m
            next_lin %= m
            prev_col %= n
            next_col %= n

            neighbors = [
                state_matrix[prev_lin, prev_col],
                state_matrix[prev_lin, col],
                state_matrix[lin, next_col],
                state_matrix[next_lin, next_col],
                state_matrix[next_lin, col],
                state_matrix[lin, prev_col],
            ]

        return neighbors

    # }}}

    @property
    def agents_neighbors(self):
        # {{{
        raise NotImplementedError("Implemented in derived class")

    # }}}

    @property
    def agents_moore_neighborhood(self):
        # {{{
        lin, col = self.pos
        neighbors = []
        for agent in self.state_list:
            if lin - 2 < agent.lin < lin + 2 and col - 2 < agent.col < col + 2:
                neighbors.append(agent)

        return neighbors

    # }}}

    @staticmethod
    def display(value):
        ...

    @staticmethod
    def from_display(rgb):
        ...

    @classmethod
    def init_from_display(cls, rgb, *args, **kwargs):
        # {{{

        return cls(cls.from_display(rgb), *args, **kwargs)

    # }}}

    def __repr__(self):
        return f"Element({self.value}, ({self.lin}, {self.col}))"


# }}}
