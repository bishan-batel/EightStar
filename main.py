BOARD_SIZE = 3


# Gets the board as input ints from the user
def input_board() -> [[int]]:
	return [
		[8, 3, 2],
		[4, 7, 1],
		[0, 5, 6]
	]
	board = test_board()
	for row in range(0, BOARD_SIZE):
		for col in range(0, BOARD_SIZE):
			board[row][col] = input(f"Enter Row {row + 1}, Column {col + 1}: ")

	return board


def clone_board(board: [[int]]) -> [[int]]:
	copy = []

	for row in board:
		copied = []
		for n in row:
			copied.append(n)
		copy.append(copied)
	return copy


def a_star_heuristic(row: int, col: int, num: int):
	# manhattan distance
	target_row, target_col = num % BOARD_SIZE, int(num / 3)
	return abs(target_row - row) + abs(target_col - col)


def get_hole_coord(board: [[int]]) -> (int, int):
	for row in range(0, BOARD_SIZE):
		for col in range(0, BOARD_SIZE):
			if board[row][col] == 0:
				return row, col


def get_possible_future_states(board: [[int]]):
	states = []

	# get 0 number row & column
	hole_row, hole_col = get_hole_coord(board)

	def add_possible_state(dx: int, dy: int):
		row = hole_row + dx
		col = hole_col + dy

		if 0 < row < BOARD_SIZE and 0 < col < BOARD_SIZE:
			clone = clone_board(board)

			clone[hole_row][hole_col] = clone[row][col]
			clone[row][col] = 0
			states.append(clone)

	add_possible_state(-1, -1)
	add_possible_state(1, -1)
	add_possible_state(1, 1)
	add_possible_state(-1, 1)


def solve():
	visited_states = []
	priority = []

	while len(priority) > 0:
		curr = priority.pop(0)
		visited_states.append(curr)



	pass
