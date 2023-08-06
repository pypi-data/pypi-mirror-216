import numpy as np

from .element import ElementTemplate

"""
Este módulo contém as classes que serão usadas para implementação de regras que
não envolvem agentes
"""


class CellMatrix:
    # {{{
    def __init__(self, state_matrix, cell_class, cell_args=None):
        # {{{
        """
        Cria a matriz de autômatos a partir de uma regra e a
        matriz de estado inicial.
        """

        self.state_matrix = state_matrix.copy()

        self.cell_args = cell_args
        if cell_args is None:
            self.cell_init = self.cell_init_nocellargs
        else:
            self.cell_init = self.cell_init_cellargs

        self.Cell = cell_class

        self.cell_matrix = np.array(
            [
                self.cell_init(value, (lin_num, col_num))
                for lin_num, lin in enumerate(self.state_matrix)
                for col_num, value in enumerate(lin)
            ]
        )

        self.display_func = np.vectorize(self.Cell.display)

    # }}}

    def update(self, *args):
        # {{{
        """
        Atualiza o estado de todas as células. Detalhe que é
        necessário copiar a matriz de estados porque matrizes do
        numpy são passadas por referência. A state_matrix é
        modificada in-place.
        """

        old_state_matrix = self.state_matrix.copy()
        self.Cell.generation_start(self.state_matrix, *args)

        for cell in self.cell_matrix:
            cell.update(old_state_matrix, *args)
            self.state_matrix[cell.pos] = cell.value

        self.Cell.generation_end(self.state_matrix, *args)

        return self.state_matrix

    # }}}

    @classmethod
    def from_display(cls, display_matrix, cell_class, cell_args=None):
        # {{{
        """
        Inicializa a partir da matriz de valores RGB ou valor de
        escala monocromática extraídos de uma imagem. Essa
        provavelmente é a maneira mais lenta possível de se fazer
        isso.
        """

        cell_from_display = cell_class.from_display
        pixels_gen = (
            cell_from_display(col) for lin in display_matrix for col in lin
        )

        state_matrix = np.array(list(pixels_gen))
        state_matrix = state_matrix.reshape(display_matrix.shape[:2])

        return cls(state_matrix, cell_class, cell_args)

    # }}}

    def display(self):
        # {{{
        """
        Retorna a matriz para representação visual do conjunto de
        células. É feio desse jeito para suportar o células
        retornando tanto inteiros (caso grayscale) quanto tuplas.
        """

        rgb_tuple = self.display_func(self.state_matrix)

        if not isinstance(rgb_tuple, tuple):
            # Isso cheira a um anti-padrão...
            rgb_tuple = (rgb_tuple, rgb_tuple, rgb_tuple)

        rgb_matrix = np.dstack(rgb_tuple).astype(np.uint8)
        return rgb_matrix

    # }}}

    def cell_init_nocellargs(self, value, pos):
        # {{{
        return self.Cell(value, pos)

    # }}}

    def cell_init_cellargs(self, value, pos):
        # {{{
        return self.Cell(value, pos, self.cell_args)

    # }}}

    def simulation_start(self, state_matrix, *args):
# {{{
        if self.cell_args is None:
            self.Cell.simulation_start(state_matrix, *args)
        else:
            self.Cell.simulation_start(
                state_matrix, *args, cell_args=self.cell_args
            )
# }}}

    @property
    def shape(self):
        return self.state_matrix.shape

    def __getitem__(self, key):
        return self.cell_matrix.reshape(self.state_matrix.shape)[key]


# }}}


class CellTemplate(ElementTemplate):
    # {{{
    """
    Um template para a implementação de células. Também define uma série de
    funções úteis que serão herdadas. Tem um monte de pylint: disable aí porque
    isso deve servir somente como uma classe template, ela não deve ser
    diretamente instanciada.
    """
    # pylint: disable=no-self-use, unused-argument

    def __repr__(self):
        return f"Cell({self.value}, ({self.lin}, {self.col}))"

    @staticmethod
    def display(value):
        # {{{
        return CellTemplate.display_binary(value)

    # }}}

    @staticmethod
    def from_display(rgb):
        # {{{

        return CellTemplate.from_binary(rgb)

    # }}}

    @staticmethod
    def display_binary(value):
        # {{{

        return 255 if value > 0 else 0

    # }}}

    @staticmethod
    def from_binary(rgb):
        # {{{

        return 1 if (rgb > 123).all() else 0

    # }}}

    @property
    def agent_above(self):
        # {{{
        for agent_tuple in self.agent_list:
            if self.pos == agent_tuple.pos:
                return agent_tuple
        return False


# }}}


# }}}
