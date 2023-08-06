import tomato as tt
import automata1D as rule
import numpy as np


# Convenience function to allow for referring to a rule by
# its decimal representation
def by_decimal_num(num):
    return tuple(bin(num).replace("0b", "").zfill(8))


cell_size = 2
size = (200, 100)

# Some rules worth checking out:
# 13, 17, 18, 28, 30, 45, 57, 60, 62, 73, 75, 89
# 102, 101, 105, 110, 129, 131, 135, 150 and 225

# 110: Turing complete
# 30: Chaotic
# 90: Siarpinsky triangle
# 184: Majority voting

rule_num = 184

# # First generation is a live cell in the middle
# state_matrix = np.zeros(size)
# state_matrix[0, size[1] // 2] = 1

# First generation is random
state_matrix = np.zeros(size)
state_matrix[0, :] = np.random.choice(2, size[1])

board = tt.Board(rule, cell_size=cell_size)
board.start(state_matrix, cell_args=by_decimal_num(rule_num))
