from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

Simple implementation of cyclic cellular automata, to test simulation_start and the
Neumann neighborhood.
"""


class CyclicCell(cell.CellTemplate):
    # {{{

    # Método executado somente uma vez no início da simulação. Neste caso, ele facilita mudar o número de estados possíveis e a vizinhança na célula de simulação.
    @classmethod
    def simulation_start(cls, state_matrix, cell_args):
        num_states = cell_args.get("num_states", 12)
        neighborhood = cell_args.get("neighborhood", "neumann")

        CyclicCell.num_states = num_states
        CyclicCell.shades = tuple(
            n * (256 // CyclicCell.num_states)
            for n in range(CyclicCell.num_states)
        )

        neighborhood = getattr(CyclicCell, f"{neighborhood}_neighborhood")
        setattr(CyclicCell, "neighbors", neighborhood)

    def update(self, state_matrix):
        self.state_matrix = state_matrix

        next_val = (self.value + 1) % CyclicCell.num_states

        if next_val in self.neighbors:
            self.value = next_val

    @staticmethod
    def display(value):
        return CyclicCell.shades[value]

    @staticmethod
    def from_display(rgb):
        return rgb[0] * (256 // CyclicCell.num_states)


# }}}
