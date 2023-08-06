import numpy as np
import tomato as tt

import random_walkers as rule

cell_size = 6
dimensions = (100, 100)
walker_list = [
    rule.WalkerTuple((255, 0, 0), (20, 20)),
    rule.WalkerTuple((0, 255, 255), (20, 80)),
    rule.WalkerTuple((255, 255, 0), (80, 20)),
    rule.WalkerTuple((255, 0, 255), (80, 80)),
]

state_matrix = np.zeros(dimensions)

board = tt.Board(rule, cell_size=cell_size, max_fps=200)
board.start(state_matrix, walker_list)
