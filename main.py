BOARD_SIZE =3


"""
Ideal Board:
0  1  2
3  4  5
6  7  8
"""

def solve():
	board = input_board(True)

	print_board(board, end="-------\n")

	visited_states = []
	priority = [(0,board_heuristic(board), board)]

	while len(priority) > 0:
		path_cost, heuristic, curr = priority.pop(0)


		if curr in visited_states:
			continue

		if heuristic == 0:
			print("Solved")
			return

		print(f"Checking pc: {path_cost}")
		print_board(curr)

		visited_states.append(curr) 

		futures = get_possible_future_states(curr)

		for future_board in get_possible_future_states(curr):
			future = ((path_cost + 1, board_heuristic(future_board), future_board))
			future_cost = future[0] + future[1]

			if len(priority) == 0:
				priority.append(future)
				continue

			for i in range(len(priority)):
				if future_cost < priority[i][0] + priority[i][1]:
					priority.insert(i, future) 
		
		# remove the highest cost heuristic
		# m = max(priority, key=lambda x: x[0] + x[1])
		# priority.remove(m)

	print("Failed to solve")


def print_board(board: [[int]], end=""):
	# print each cell of the board in a grid

	# print top bar 
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			cell = board[row][col]
			print(" " if cell == 0 else cell, end="  ")
		print()
	print(end)

def create_board() -> [[int]]:
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
def input_board(test=False) -> [[int]]:
	if (test):
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
	target_row, target_col = num // BOARD_SIZE,  num % BOARD_SIZE
	return abs(target_row - row) + abs(target_col - col)
	return num

def board_heuristic(board: [[int]]) -> int:
	heuristic = 0

	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			heuristic += board_cell_heuristic(row, col, board[row][col])
	return heuristic


def get_hole_coord(board: [[int]]) -> (int, int):
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if board[row][col] == 0:
				return row, col


def get_possible_future_states(board: [[int]]):
	states = []

	# get 0 number row & column
	hole_row, hole_col = get_hole_coord(board)

	position_deltas = [
		(-1, 0), # up
		(1, 0), # down
		(0, -1), # left
		(0, 1), # right
	]

	for dx, dy in position_deltas:
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
			states.append(clone)
		
	return states

solve()