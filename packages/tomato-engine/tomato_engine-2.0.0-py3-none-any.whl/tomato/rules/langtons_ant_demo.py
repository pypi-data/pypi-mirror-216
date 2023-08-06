import numpy as np
import tomato as tt

import langtons_ant as rule

cell_size = 4
dimensions = (100, 100)
ant_list = [
    rule.AntTuple((1, 0), (50, 50)),
    # rule.AntTuple((0, 1), (150, 50)),
]

state_matrix = np.ones(dimensions)

board = tt.Board(rule, cell_size=cell_size, debug=False, max_fps=300)
board.start(
    state_matrix,
    ant_list,
    show_window=True,
)
