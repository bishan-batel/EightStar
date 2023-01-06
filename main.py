BOARD_SIZE = 3
POSSIBLE_DELTAS = [
	(-1, 0, "Up"),  # up
	(1, 0, "Down"),  # down
	(0, -1, "Left"),  # left
	(0, 1, "Right"),  # right
]

"""
Ideal Board:
0  1  2
3  4  5
6  7  8
"""


def solve():
	board = input_board(True)

	print_board(board, end="-------\n")

	initial_heuristic = board_heuristic(board)
	if initial_heuristic % 2 == 1:
		print("This board is not solvable.")
		return

	visited_states = []
	priority = [
		(0, initial_heuristic, board)
	]

	while len(priority) > 0:
		depth, cost, board = priority.pop(0)
		visited_states.append(board)

		if cost == 0:
			print("Solved")
			return

		# get futures that has not been visited before
		futures = list(filter(lambda f: f[0] not in visited_states, get_possible_future_states(board)))

		for future in futures:
			add_to_priority_queue(priority, (depth + 1, board_heuristic(future[0]), future[0]), lambda f: f[0] + f[1])
	# remove the highest cost heuristic
	# m = max(priority, key=lambda x: x[0] + x[1])
	# priority.remove(m)

	print("Failed to solve")


def add_to_priority_queue(queue: list, to_add, key=lambda x: x):
	to_add = key(to_add)

	for i in range(len(queue)):
		if key(queue[i]) > key(to_add):
			queue.insert(i, to_add)
			return
	raise "huh"


def print_board(board, end=""):
	# print each cell of the board in a grid

	# print top bar 
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			cell = board[row][col]
			print(" " if cell == 0 else cell, end="  ")
		print()
	print(end)


def create_board():
	board = []

	for r in range(BOARD_SIZE):
		row = []
		for c in range(BOARD_SIZE):
			row.append(r * BOARD_SIZE + c)
		board.append(row)
	return board


def clone_board(board: [[int]]) -> [[int]]:
	copy = []

	for row in board:
		copied = []
		for n in row:
			copied.append(n)
		copy.append(copied)
	return copy


# Gets the board from the user, or test data if asked
def input_board(test=False):
	if test:
		return [
			[8, 3, 2],
			[4, 7, 1],
			[0, 5, 6]
		]

	board = create_board()
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			board[row][col] = input(f"Enter Row {row + 1}, Column {col + 1}: ")

	return board


def board_cell_heuristic(row: int, col: int, num: int):
	# manhattan distance
	target_row, target_col = num // BOARD_SIZE, num % BOARD_SIZE
	return abs(target_row - row) + abs(target_col - col)


def board_heuristic(board) -> int:
	heuristic = 0

	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			heuristic += board_cell_heuristic(row, col, board[row][col])
	return heuristic


def get_hole_coord(board: list[list[int]]) -> (int, int):
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if board[row][col] == 0:
				return row, col


def get_possible_future_states(board):
	states = []

	# get 0 number row & column
	hole_row, hole_col = get_hole_coord(board)

	for dx, dy, name in POSSIBLE_DELTAS:
		row = hole_row + dx
		col = hole_col + dy

		# check if the hole can swap in that direction
		if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
			# clone the board for hte new state
			clone = clone_board(board)

			# swap the hole with the cell to swap with
			clone[hole_row][hole_col] = clone[row][col]
			clone[row][col] = 0
			# add to states
			states.append((clone, name))

	return states


solve()
