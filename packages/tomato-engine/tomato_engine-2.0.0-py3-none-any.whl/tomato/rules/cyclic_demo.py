import tomato as tt
from tomato.functions import utils
import cyclic as rule

CELL_SIZE = 5
DIMENSIONS = (120, 120)

# Experimente alterar o número de estados e a vizinhança
NUM_STATES = 10
NEIGHBORHOOD = "neumann"
CELL_ARGS = {"num_states": NUM_STATES, "neighborhood": NEIGHBORHOOD}

initial_state = utils.random_int_matrix(DIMENSIONS, NUM_STATES)

board = tt.Board(rule, cell_size=CELL_SIZE)
board.start(initial_state, cell_args=CELL_ARGS)
