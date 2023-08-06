from collections import namedtuple

from tomato.classes import agent, cell

AntTuple = namedtuple("AntTuple", ["dir", "pos"])


class BackgroundCell(cell.CellTemplate):
    # {{{
    def update(self, state_matrix, agent_list):
        self.agent_list = agent_list

        agent_above = self.agent_above

        if agent_above:
            self.value = not self.value


# }}}


class Ant(agent.AgentTemplate):
    # {{{
    def update(self, state_matrix, agent_list):
        self.state_matrix = state_matrix

        if self.cell_below:  # white cell
            self.value = (  # turn counter-clockwise
                self.value[1],
                -self.value[0],
            )

        else:  # black cell
            self.value = (-self.value[1], self.value[0])  # turn clockwise

        self.move(state_matrix)

    def move(self, state_matrix):
        m, n = state_matrix.shape

        self.lin = (self.lin + self.value[0]) % m
        self.col = (self.col + self.value[1]) % n

    @staticmethod
    def display(value):
        return (255, 0, 0)


# }}}
