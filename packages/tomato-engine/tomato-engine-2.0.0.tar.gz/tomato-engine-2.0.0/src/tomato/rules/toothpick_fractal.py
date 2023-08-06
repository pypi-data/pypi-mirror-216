from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

The 'toothpick fractal' featured on episode 'Terrific Toothpick Patterns' of
Numberphile. The Von Neumann neighborhood version of this rule is known as the
Ulam-Warbuton Cellular Automaton. Included this mainly because it's a notable and fun
rule.
"""


class ToothpickCell(cell.CellTemplate):
    # {{{
    @classmethod
    def simulation_start(cls, state_matrix, cell_args):
        neighborhood = getattr(ToothpickCell, f"{cell_args}_neighborhood")
        setattr(ToothpickCell, "neighbors", neighborhood)

    def update(self, state_matrix):
        self.state_matrix = state_matrix

        if sum(self.neighbors) == 1:  # only one live neighbor
            self.value = 1


# }}}
