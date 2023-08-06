import tomato as tt
from tomato.functions import utils
import tomato_life as rule

CELL_SIZE = 4
dimensions = (100, 100)
state_matrix = utils.random_choice_matrix(dimensions, (0, 2, 1, 3))

board = tt.Board(rule, cell_size=CELL_SIZE)

board.start(state_matrix)
# board.start("images/tomato-logo.png", paused=True)
