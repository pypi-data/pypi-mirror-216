import numpy as np
from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

This is an implementation of 1D cellular automata. Even though tomato-engine
was conceived as an engine specifically for 2D cellular automata, it is
flexible enough to allow an implementation of 1D cellular automata with
arbitrary rules as a simple Cell class, just like any other rule.
"""


class Cell1D(cell.CellTemplate):
    # {{{

    # Todas as combinações possíveis de estados da célula e das vizinhas, de
    # acordo com a notação de Wolfram.
    possible_states = [  # {{{
        [1, 1, 1],  # rule_array[0]
        [1, 1, 0],  # rule_array[1]
        [1, 0, 1],  # rule_array[2]
        [1, 0, 0],  # rule_array[3]
        [0, 1, 1],  # rule_array[4]
        [0, 1, 0],  # rule_array[5]
        [0, 0, 1],  # rule_array[6]
        [0, 0, 0],  # rule_array[7]
    ]  # }}}

    @classmethod
    def simulation_start(cls, state_matrix, cell_args):
        Cell1D.rule_tuple = cell_args

        Cell1D.generation = 0

    def update(self, state_matrix):
        # {{{
        self.state_matrix = state_matrix

        if self.lin == self.generation + 1:
            for i, state in enumerate(Cell1D.possible_states):
                if np.array_equal(state, self.neighbors):
                    self.value = Cell1D.rule_tuple[i]
        self.generation += 1

    # }}}

    # Este é o primeiro exemplo de definição própria da vizinhança. Note como
    # usamos self.lin e self.col (linha e coluna da célula) para encontrar as
    # suas vizinhas
    @property
    def neighbors(self):
        # {{{
        state_matrix = self.state_matrix
        m, n = state_matrix.shape

        prev_lin = self.lin - 1

        # Dividimos por n (número de colunas) aqui para que as células das
        # bordas considerem como vizinhas as células no outro lado da matriz.
        # Ou seja, topologia toroidal
        prev_col = (self.col - 1) % n
        next_col = (self.col + 1) % n

        return [
            state_matrix[prev_lin, prev_col],
            state_matrix[prev_lin, self.col],
            state_matrix[prev_lin, next_col],
        ]


# }}}

# }}}
