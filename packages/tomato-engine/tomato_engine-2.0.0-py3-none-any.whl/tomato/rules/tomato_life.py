from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

This is 3 variations of Conway's Game of Life at the same time, presumably different
species fighting for survival. These 'species' are: White (B3/S23), Red (B3/S238), and
Green (B36/S23), where the numbers after B denote with how many live neighbors cell is
born and the numbers after S similarly denote the survival conditions. In this
particular implementation, the 'birth' priority from a dead cell is white -> red ->
green, and the 'birth' priority from a living cell depends on its species: white beats
red beats green beats white.

This rule can be run with images/tomato-logo.png as its initial state, with interesting
results.
"""


class Cell(cell.CellTemplate):
    # {{{

    # Dead: 0
    # White: 1, B3/S23
    # Red: 2, B3/S238
    # Green: 3, B36/S23

    # Dead: white > red > green
    # Live: white > red > green > white

    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell
        if self.value == 0:
            if self.live_green_neighbors in (3, 6):
                self.value = 3
            elif self.live_red_neighbors == 3:
                self.value = 2
            elif self.live_white_neighbors == 3:
                self.value = 1
            else:
                self.value = 0

        # White cell
        elif self.value == 1:
            if self.live_red_neighbors == 3:
                self.value = 2
            elif self.live_white_neighbors in (2, 3):
                self.value = 1
            elif self.live_green_neighbors in (3, 6):
                self.value = 3
            else:
                self.value = 0

        # Red cell
        elif self.value == 2:
            if self.live_green_neighbors in (3, 6):
                self.value = 3
            elif self.live_red_neighbors in (2, 3, 8):
                self.value = 2
            elif self.live_white_neighbors == 3:
                self.value = 1
            else:
                self.value = 0

        # Green cell
        elif self.value == 3:
            if self.live_white_neighbors == 3:
                self.value = 1
            elif self.live_green_neighbors in (2, 3):
                self.value = 3
            elif self.live_red_neighbors == 3:
                self.value = 2
            else:
                self.value = 0

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_white_neighbors(self):
        return self.neighbors.count(1)

    @property
    def live_green_neighbors(self):
        return self.neighbors.count(3)

    @property
    def live_red_neighbors(self):
        return self.neighbors.count(2)

    @staticmethod
    def display(value):
        if value == 1:
            return (255, 255, 255)
        elif value == 2:
            return (255, 0, 0)
        elif value == 3:
            return (0, 255, 0)
        else:
            return (0, 0, 0)

    @staticmethod
    def from_display(value):
        if (value == (255, 255, 255)).all():
            return 1
        elif (value == (255, 0, 0)).all():
            return 2
        elif (value == (0, 255, 0)).all():
            return 3
        else:
            return 0


# }}}
