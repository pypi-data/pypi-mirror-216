import os
from time import time
from types import ModuleType

import numpy as np
from IPython import display

from ..functions import file_io
from ..functions.handling_rules import agent_from_rule, cell_from_rule
from .agent import AgentList
from .cell import CellMatrix
from .window import Window


class Board:
    # {{{
    """
    O nome dessa classe é vago, mas ela é importante. Esta é a interface do
    usuário, e também coordena a CellMatrix e a Window.
    """

    # The default configs for Board
    config_dict = {
        "show_window": True,
        "paused": False,
        "generations": None,
        "inline": False,
        "generate_figures": False,
        "generate_figures_dir": f"AutomataSimulation{os.path.sep}",
        "generate_gif": False,
        "step": None,
        "debug": False,
        "title": "Simulation",
        "max_fps": 60,
        "cell_size": 4,
    }

    def __init__(self, rule, rule_agents=None, **kwargs):
        # {{{
        """
        Recebe a regra a ser adotada, assim como algumas configurações. A
        simulação em si começa com a função start.

        A rule é o módulo importado contendo a regra, no formato
        especificado pelo exemplo game_of_life.py.

        Se só o argumento `rule` for passado, entende-se que isso é ou um
        módulo contendo a classe Cell e a Agent, ou é a própria classe
        Cell, ou um módulo só com a Cell.
        """

        if isinstance(rule, ModuleType):
            try:  # checks if Agents class is present
                agent_class = agent_from_rule(rule)
                cell_class = cell_from_rule(rule)
                self.backend = BoardBackendAgents(
                    cell_class, agent_class, **kwargs
                )
            except TypeError:  # then assumes the module contains only Cell
                cell_class = cell_from_rule(rule)
                self.backend = BoardBackendCells(cell_class, **kwargs)
        else:  # then it must be a Cell class
            cell_class = cell_from_rule(rule)
            if rule_agents is not None:
                agent_class = agent_from_rule(rule_agents)
                self.backend = BoardBackendAgents(
                    cell_class, agent_class, **kwargs
                )
            else:
                self.backend = BoardBackendCells(cell_class, **kwargs)

        # Then set all frontend methods to be the BoardBackend equivalents
        self.load_state = self.backend.load_state


        # Configurações opcionais são passadas por kwargs.
        self.config_dict = Board.config_dict.copy()
        self.update_config(kwargs)

        if self.debug:
            # Lista com o tempo transcorrido para cada geração
            self.gen_time = []

    # }}}

    def update(self):
        # {{{
        if self.generate_figures:
            if self.step is None:
                self.save_png()
            else:
                if self.backend.generation % self.step == 0:
                    self.save_png()
        if self.inline:
            display.clear_output(wait=True)
            display.display(file_io.img(self.display_matrix, self.cell_size))

        if not self.debug:
            self.backend.update()
        else:
            initial_time = time()
            self.backend.update()
            self.gen_time.append(1000.0 * (time() - initial_time))

    # }}}

    def start(self, *args, **kwargs):
        # {{{
        """
        Inicia a simulação, o estado inicial das células sendo dado pelo
        primeiro argumento. state_matrix pode ser o caminho para uma imagem
        ou uma matriz de numpy com os valores desejados.
        """

        self.update_config(kwargs)

        if self.generate_gif:
            self.generate_figures = True
            if self.generations is None:
                raise TypeError(
                    "You must specify the number of generations for "
                    "the gif to be created."
                )

        if self.generate_figures:
            self.check_dir(self.generate_figures_dir)

        # We expect state_matrix to be the first and only argument if the
        # backend is BoardBackendCells
        # And if it is BoardBackendAgents, state_matrix is the first argument
        # and state_list to be the second
        # cell_args is amongst the kwargs here
        self.backend.start(*args, **kwargs)

        if self.inline or not self.show_window:
            self.mainloop()
        else:
            self.start_window()

    # }}}

    def resume(self, **kwargs):
        # {{{
        """
        Continua a simulação de onde ela parou.
        """

        self.update_config(kwargs)

        if self.generate_gif:
            self.generate_figures = True
            if self.generations is None:
                raise TypeError(
                    "You must specify the number of generations for "
                    "the gif to be created."
                )

        if self.generate_figures:
            self.check_dir(self.generate_figures_dir)

        if self.inline or not self.show_window:
            self.mainloop()
        else:
            self.start_window()

    # }}}

    def start_window(self, paused=None):
        # {{{
        """
        Começa a simulação, mostrando a janelinha.
        """

        if paused is None:
            try:
                paused = self.paused
            except AttributeError:
                paused = False

        window = Window(
            self.display_matrix,
            debug=self.debug,
            title=self.title,
            paused=paused,
            max_fps=self.max_fps,
            cell_size=self.cell_size,
        )

        while window.running:
            window.query_inputs()

            if window.paused is False:
                self.update()
                window.update(self.display_matrix)

                if self.debug:
                    self.print_debug()

                try:
                    if self.generations is not None:
                        if self.backend.generation >= self.generations:
                            window.running = False
                        if self.backend.generation == self.generations:
                            if self.generate_gif:
                                self.save_gif()
                except AttributeError:
                    pass

        if self.debug:
            self.print_avg_update_time()

        # Para lembrar como o usuário deixou a janela
        self.paused = window.paused
        self.max_fps = window.max_fps

        window.quit()

    # }}}

    def mainloop(self):
        # {{{
        """
        Começa a simulação, sem mostrar a janelinha. Note aqui que
        self.backend.generations eh o numero de geracoes da simulacao e
        self.generations eh o numero maximo de geracoes
        """

        running = True
        while running:
            try:
                self.update()
            except KeyboardInterrupt:
                break

            if self.debug:
                self.print_debug()

            if self.generations is not None:
                if self.backend.generation >= self.generations:
                    running = False
                if self.backend.generation == self.generations:
                    if self.generate_gif:
                        self.save_gif()

        if self.debug:
            self.print_avg_update_time()

    # }}}

    def print_debug(self):
        # {{{
        """
        Auto-explicativo. Printa as informações de depuração.
        """

        print(
            "| {:<16} {:<8} | {:<16} {:<8.4f} ms |".format(
                "Generation:",
                self.generation,
                "Generation time:",
                self.gen_time[-1],
            )
        )

    # }}}

    def print_avg_update_time(self):
        # {{{
        """
        Método bem específico. Printa o tempo médio das gerações
        e o desvio padrão.
        """

        print(
            "| Average generation time: {} +- {} ms |".format(
                np.mean(self.gen_time),
                np.std(self.gen_time),
            )
        )

    # }}}

    def save_png(self, path=None):
        # {{{
        """
        Salva o estado da cellMatrix em uma png, para
        visualização e para retomar a simulação depois.
        """

        if path is None:
            path = f"{self.generate_figures_dir}{self.generation}.png"
        elif isinstance(path, str):
            if path.endswith(f"{os.path.sep}"):
                path = f"{path}{self.generation}.png"
            elif not path.endswith(".png"):
                path = f"{path}{os.path.sep}{self.generation}.png"

        file_io.save_png(
            path, self.display_matrix, self.cell_size, print_output=False
        )

    # }}}

    def save_gif(self, path=None, max_fps=60):
        # {{{
        """
        Salva o estado da cellMatrix em uma png, para
        visualização e para retomar a simulação depois.
        """
        if path is None:
            path = f"{self.generate_figures_dir}"

        file_io.save_gif(path, fps=self.max_fps)

    # }}}

    def check_dir(self, add=0):
        # {{{
        """
        Função para checar se o diretório existe e renomear
        com números inteiros em sequência para a criação de outro diretório.
        """
        i = 1
        dir = self.generate_figures_dir
        if dir is None:
            dir = f"{self.title}{os.path.sep}"
        if not dir.endswith(f"{os.path.sep}"):
            dir = f"{dir}{os.path.sep}"
        while os.path.isdir(dir):
            num = "%03d" % i
            dir = (
                f"{dir.split(os.path.sep)[0].split('_')[0]}_{num}{os.path.sep}"
            )
            i += 1
        os.mkdir(dir)
        self.generate_figures_dir = dir

    # }}}

    def current_time_millis(self):
        # {{{
        """
        Função auxiliar para retornar o tempo UNIX em milissegundos
        arredondado.
        """
        return round(time() * 1000)

    # }}}

    @property
    def state_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz de estados.
        """

        return self.backend.state_matrix

    # }}}

    @property
    def display_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz display.
        """

        return self.backend.display_matrix

    # }}}

    @property
    def generation(self):
        return self.backend.generation

    def update_config(self, config_dict):
        # {{{
        """
        Since I never seem to know whether to pass a kwarg on start or init,
        why not make it so they can be passed on either?
        """

        self.config_dict.update(config_dict)

        for key, val in self.config_dict.items():
            setattr(self, key, val)


# }}}


# }}}


class BoardBackendCells:
    # {{{
    def __init__(self, cell_class, **kwargs):
        # {{{
        # And the prize for the stupidest hack of the year goes to...
        self.img_cell_size = kwargs.get(
            "img_cell_size", kwargs.get("cell_size", 1)
        )

        self.cell_class = cell_class

    # }}}

    def start(self, state_matrix, **kwargs):
        # {{{
        """
        Inicia a simulação, o estado inicial sendo dado pela
        state_matrix. state_matrix pode ser o caminho para uma
        imagem ou uma matriz de numpy com os valores desejados.

        O abuso de *args e **kwargs aqui e insano
        """

        cell_args = kwargs.get("cell_args", None)
        self.load_state(
            state_matrix, cell_args=cell_args, img_cell_size=self.img_cell_size
        )
        self.cellMatrix.simulation_start(state_matrix)

    # }}}

    def update(self):
        # {{{
        """
        Atualiza o estado da simulação, ou seja, realiza uma nova iteração.
        """
        self.cellMatrix.update()
        self.generation += 1

    # }}}

    def load_state(self, state_matrix, cell_args=None, img_cell_size=1):
        # {{{
        """
        Carrega uma matriz de estados a partir de uma imagem, uma
        matriz numpy ou uma lista de listas.
        """

        self.generation = 0

        if isinstance(state_matrix, str):
            png_matrix = file_io.load_png(state_matrix, size=img_cell_size)
            self.cellMatrix = CellMatrix.from_display(
                png_matrix, self.cell_class, cell_args=cell_args
            )
        elif isinstance(state_matrix, np.ndarray):
            self.cellMatrix = CellMatrix(
                state_matrix, self.cell_class, cell_args=cell_args
            )
        elif isinstance(state_matrix, list):
            state_matrix = np.array(state_matrix)
            self.cellMatrix = CellMatrix(
                state_matrix, self.cell_class, cell_args=cell_args
            )
        else:
            raise TypeError(
                f"{type(state_matrix)} is not a valid type for a state "
                "matrix."
            )

    # }}}

    @property
    def state_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz de estados.
        """

        return self.cellMatrix.state_matrix

    # }}}

    @property
    def display_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz display.
        """

        return self.cellMatrix.display()

    # }}}


# }}}


class BoardBackendAgents:
    # {{{
    def __init__(self, cell_class, agent_class, **kwargs):
        # {{{
        # And the prize for the stupidest hack of the year goes to...
        self.img_cell_size = kwargs.get(
            "img_cell_size", kwargs.get("cell_size", 1)
        )

        self.cell_class = cell_class
        self.agent_class = agent_class

    # }}}

    def start(self, state_matrix, state_list, *args, **kwargs):
        # {{{
        """
        Inicia a simulação, o estado inicial sendo dado pela
        state_matrix. state_matrix pode ser o caminho para uma
        imagem ou uma matriz de numpy com os valores desejados.

        O abuso de *args e **kwargs aqui e insano
        """

        cell_args = kwargs.get("cell_args", None)
        self.load_state(
            state_matrix,
            state_list,
            cell_args=cell_args,
            img_cell_size=self.img_cell_size,
        )
        self.cellMatrix.simulation_start(state_matrix, state_list)
        self.agentList.simulation_start(state_matrix, state_list)

        # this is stupid, is used just to keep track of the agents spawn queue
        self.cell_instance = self.cellMatrix[0, 0]

    # }}}

    def update(self):
        # {{{
        """
        Atualiza o estado da simulação, ou seja, realiza uma nova iteração.
        """
        old_state_list = self.agentList.state_list.copy()

        for i in range(len(self.cell_instance._agent_spawn_queue)):
            self.agentList.spawn_agent(
                self.cell_instance._agent_spawn_queue[i]
            )
            self.cell_instance._agent_spawn_queue.pop(i)

        self.agentList.update(self.cellMatrix.state_matrix)
        self.cellMatrix.update(old_state_list)

        # self.cell_instance._agent_spawn_queue = []

        self.generation += 1

    # }}}

    def load_state(
        self, state_matrix, state_list=None, cell_args=None, img_cell_size=1
    ):
        # {{{
        """
        Carrega uma matriz de estados a partir de uma imagem, uma
        matriz numpy ou uma lista de listas.
        """

        self.generation = 0

        if isinstance(state_matrix, str):
            png_matrix = file_io.load_png(state_matrix, size=img_cell_size)
            self.cellMatrix = CellMatrix.from_display(
                png_matrix, self.cell_class, cell_args=cell_args
            )
            self.agentList = AgentList.from_display(
                png_matrix, self.agent_class, cell_args=cell_args
            )
        elif isinstance(state_matrix, (np.ndarray, list)):
            if isinstance(state_matrix, list):
                state_matrix = np.array(state_matrix)
            self.cellMatrix = CellMatrix(
                state_matrix, self.cell_class, cell_args=cell_args
            )
            if state_list is None:
                raise TypeError(
                    "Agent's list of initial states (state_list) not "
                    "provided to BoardBackendAgents.load_state."
                )
            elif isinstance(state_list, list):
                self.agentList = AgentList(
                    state_list, self.agent_class, cell_args=cell_args
                )
            else:
                raise TypeError(
                    f"{type(state_matrix)} is not a valid type for a state "
                    "matrix."
                )

    # }}}

    @property
    def state_matrix(self):
        return self.cellMatrix.state_matrix

    @property
    def state_list(self):
        return self.agentList.state_list

    @property
    def display_matrix(self):
        # {{{

        display_matrix = self.cellMatrix.display()
        agent_display_list = self.agentList.display()

        for agent in agent_display_list:
            display_matrix[agent.pos] = agent.rgb_tuple

        return display_matrix

    # }}}


# }}}
