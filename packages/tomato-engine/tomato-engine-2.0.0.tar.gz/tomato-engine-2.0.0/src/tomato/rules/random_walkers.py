from random import choice

from tomato.classes import agent, cell
from collections import namedtuple

WalkerTuple = namedtuple("WalkerTuple", ["val", "pos"])

class BackgroundCell(cell.CellTemplate):
    # {{{
    def update(self, state_matrix, state_list):
        self.agent_list = state_list
        if self.agent_above:
            self.value = 100
        else:
            self.value -= 2
            if self.value < 0:
                self.value = 0

    @staticmethod
    def display(value):
        return (value, value, value)

# }}}


class Walker(agent.AgentTemplate):
# {{{
    def update(self, state_matrix, state_list):
        dirlin = choice((-1, 0, 1))
        dircol = choice((-1, 0, 1))

        m, n = state_matrix.shape
        self.lin = (self.lin + dirlin) % m
        self.col = (self.col + dircol) % n

    # The Agent's color is its value. So initialize them with RGB tuples
    @staticmethod
    def display(value):
        return value
# }}}
