from time import time

BOARD_SIZE = 3
POSSIBLE_DELTAS = [
	(-1, 0, "U"),  # up
	(1, 0, "D"),  # down
	(0, -1, "L"),  # left
	(0, 1, "R"),  # right
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

	visited_states = {}

	priority = [
		(0, initial_heuristic, board, "")
	]

	while len(priority) > 0:
		depth, cost, board, path = priority.pop(0)

		visited_states[board_hash(board)] = True
		# visited_states.append(board)

		# get futures that has not been visited before
		future_depth = depth + 1
		for future in get_possible_future_states(board):
			if board_hash(future[0]) in visited_states:
				continue
			# print(priority)
			heuristic = board_heuristic(future[0])

			if heuristic == 0:
				print_board_path(path)
				print("Solved")
				return

			to_add = (future_depth, heuristic, future[0], f"{path}{future[1]}")
			cost = to_add[0] + to_add[1]

			for i, ele in enumerate(priority):
				if ele[0] + ele[1] > cost:
					priority.insert(i, to_add)
					break
			else:
				priority.append(to_add)

	# if len(priority) > 0:
	# 	m = max(priority, key=lambda x: x[0] + x[1])
	# 	priority.remove(m)

	print("Failed to solve")


def print_board_path(path):
	for p in path:
		match p:
			case "U":
				print("Up", end=", ")
			case "D":
				print("Down", end=", ")
			case "L":
				print("Left", end=", ")
			case "R":
				print("Right", end=", ")
	print()


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
		# copied = []
		# for n in row:
		# 	copied.append(n)
		# copy.append(copied)
		copy.append(row.copy())
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

	# for dx, dy, name in POSSIBLE_DELTAS:
	# 	row = hole_row + dx
	# 	col = hole_col + dy
	#
	# 	# check if the hole can swap in that direction
	# 	if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
	# 		# clone the board for hte new state
	# 		clone = clone_board(board)
	#
	# 		# swap the hole with the cell to swap with
	# 		clone[hole_row][hole_col] = clone[row][col]
	# 		clone[row][col] = 0
	# 		# add to states
	# 		states.append((clone, name))

	if hole_row > 0:
		clone = clone_board(board)
		clone[hole_row][hole_col] = clone[hole_row - 1][hole_col]
		clone[hole_row - 1][hole_col] = 0
		states.append((clone, "L"))

	if hole_row < BOARD_SIZE - 1:
		clone = clone_board(board)
		clone[hole_row][hole_col] = clone[hole_row + 1][hole_col]
		clone[hole_row + 1][hole_col] = 0
		states.append((clone, "R"))

	if hole_col > 0:
		clone = clone_board(board)
		clone[hole_row][hole_col] = clone[hole_row][hole_col - 1]
		clone[hole_row][hole_col - 1] = 0
		states.append((clone, "U"))

	if hole_col < BOARD_SIZE - 1:
		clone = clone_board(board)
		clone[hole_row][hole_col] = clone[hole_row][hole_col + 1]
		clone[hole_row][hole_col + 1] = 0
		states.append((clone, "D"))

	return states


def board_hash(board: list[list[int]]):
	check_sum = ""
	for row in board:
		for cell in row:
			check_sum += str(cell)
	return check_sum


solve()
