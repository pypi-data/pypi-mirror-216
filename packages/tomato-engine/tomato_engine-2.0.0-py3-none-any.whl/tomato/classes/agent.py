from collections import namedtuple

from .element import ElementTemplate

AgentTuple = namedtuple("AgentTuple", ["value", "pos"])
AgentDisplayTuple = namedtuple("AgentDisplayTuple", ["rgb_tuple", "pos"])

"""
Este módulo contém as classes que serão usadas para implementação de regras que
envolvem agentes
"""


class AgentList:
    # {{{
    def __init__(self, state_list, agent_class, cell_args=None):
        # {{{
        """
        Cria a matriz de autômatos a partir de uma regra e a
        matriz de estado inicial.
        """

        self.state_list = state_list.copy()

        self.cell_args = cell_args
        if cell_args is None:
            self.agent_init = self.agent_init_no_cellargs
        else:
            self.agent_init = self.agent_init_cellargs

        self.Agent = agent_class

        self.agent_list = [self.agent_init(agent) for agent in state_list]

        self.display_func = self.Agent.display

    # }}}

    def update(self, state_matrix):
        # {{{

        self.Agent.generation_start(state_matrix, self.state_list)

        new_state_list = []
        for agent in self.agent_list:
            agent.update(state_matrix, self.state_list)
            if not agent._despawn_flag:
                new_state_list.append(AgentTuple(agent.value, agent.pos))

        self.Agent.generation_end(state_matrix, self.state_list)

        self.state_list = new_state_list

        return self.state_list

    # }}}

    @classmethod
    def from_display(cls, display_matrix, agent_class, cell_args=None):
        # {{{
        """
        Inicializa a partir da matriz de valores RGB ou valor de
        escala monocromática extraídos de uma imagem. Essa
        provavelmente é a maneira mais lenta possível de se fazer
        isso.
        """

        agent_from_display = agent_class.from_display

        state_list = []
        for lin, pixel_lin in enumerate(display_matrix):
            for col, pixel in enumerate(pixel_lin):
                value = agent_from_display(pixel)
                if value is not None:
                    agentTuple = AgentTuple(value, (lin, col))
                    state_list.append(agentTuple)

        return cls(state_list, agent_class, cell_args)

    # }}}

    def display(self):
        # {{{

        # This could and probably should be done by the Agent.display itself
        display_list = [
            AgentDisplayTuple(self.display_func(agent[0]), agent[1])
            for agent in self.state_list
        ]

        return display_list

    # }}}

    def simulation_start(self, state_matrix, state_list):
        # {{{
        if self.cell_args is None:
            self.Agent.simulation_start(state_matrix, state_list)
        else:
            self.Agent.simulation_start(
                state_matrix, state_list, self.cell_args
            )

    # }}}

    def spawn_agent(self, agent_tuple):
        # {{{
        self.agent_list.append(self.agent_init(agent_tuple))

    # }}}

    def agent_init_cellargs(self, agent_tuple):
        # {{{
        return self.Agent(agent_tuple[0], agent_tuple[1], self.cell_args)

    # }}}

    def agent_init_no_cellargs(self, agent_tuple):
        # {{{
        return self.Agent(agent_tuple[0], agent_tuple[1])

    # }}}

    @property
    def agents_num(self):
        return len(self.state_list)

    def __getitem__(self, key):
        return self.agent_list[key]


# }}}


class AgentTemplate(ElementTemplate):
    # {{{
    _despawn_flag = False

    def despawn(self):
        self._despawn_flag = True

    @staticmethod
    def display(value):
        # {{{

        return (255, 0, 0)

    # }}}

    @staticmethod
    def from_display(rgb):
        # {{{
        # Agent.from_display will have to be of this form

        if rgb == (255, 0, 0):
            return 1
        else:
            return None

    # }}}

    def __repr__(self):
        return f"Agent({self.value}, ({self.lin}, {self.col}))"

    @property
    def cell_below(self):
        return self.state_matrix[self.pos]
# }}}
