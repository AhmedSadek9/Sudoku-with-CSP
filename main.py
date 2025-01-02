import numpy as np
import copy
import time

def is_valid_move(board, row, col, num): # input number and its index
    if num in board[row]:  # check if number is not repeated in the same row
        return False
    # check if number is not repeated in the same column
    if num in [board[i][col] for i in range(9)]: # iterate every row in specific column
        return False

    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3): # check if number is not repeated in the 3x3 subgrid
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False

    return True


def is_empty_cell(board): # empty cell with least domain
    min_remaining_values = float('inf')
    selected_cell = None
    for i in range(9): # iterate every row and column
        for j in range(9):
            if board[i][j] == 0: # if cell is empty
                remaining_values = len(get_domain_values(board, i, j)) # count number of domain
                if remaining_values < min_remaining_values:
                    min_remaining_values = remaining_values # choose cell with least domain value
                    selected_cell = (i, j)
    return selected_cell


def backtracking(board):
    empty_cell = is_empty_cell(board) # empty minimum domain cell
    print(f"MRV is {empty_cell}")
    if empty_cell is None: # board is full
        return True

    row, col = empty_cell # index of least domain value
    domain_values = get_domain_values(board, row, col) # get domain of the least domain
    domain_values.sort(key=lambda num: count_constrained_values(board, row, col, num)) # for every domain, calculate no. of constraints ascending #LCV
    print(f"Trying to fill cell ({row}, {col}) with domain values: {domain_values}") # fill the MRV with its domain

    for num in domain_values:
        print(f"Trying value {num} for cell ({row}, {col})") # try first domain
        if is_valid_move(board, row, col, num):
            board[row][col] = num # assign
            print("Applying forward checking") # detection of failure
            if apply_arc_consistency(board) is not None: # new board after trying first domain
                print("Forward checking successful")
                if backtracking(board): # check if empty cells is none
                    return True
            print(f"Value {num} for cell ({row}, {col}) leads to conflict. Backtracking...") # does not apply arc consistency
            board[row][col] = 0
        else: # not valid move
            print(f"Value {num} is not valid for cell ({row}, {col}). Skipping...")

    print(f"No valid value found for cell ({row}, {col}). Backtracking...") # backtracking
    return False

def get_domain_values(board, row, col):  #domain value for given cell
        domain_values = [num for num in range(1, 10) if is_valid_move(board, row, col, num)] #try from 1 to 9, add valid number
        return domain_values #option in given cells


def count_constrained_values(board, row, col, num):  # number of constrained in given cell
        count = 0  # number can not appear more than one in same row or column
        for i in range(9):
            if i != col and not is_valid_move(board, row, i, num):  # loop on every cell in same row
                count += 1  # cells have same number
            if i != row and not is_valid_move(board, i, col, num):  # loop on every cell in same column
                count += 1  # no. of cells have same number
        for i in range(row - row % 3, row - row % 3 + 3): # start and end row of subgrid
            for j in range(col - col % 3, col - col % 3 + 3): # start and end column of subgrid
                if (i != row or j != col) and not is_valid_move(board, i, j, num): # loop on every cell in subgrid
                    count += 1  # cell that violate constraints in same subgrid
        return count

def forward_checking(board, row, col, num):
    # original_board = copy.deepcopy(board)  #copy of board

    board[row][col] = num # assign

    # Check consistency
    for i in range(9):
        if i != col and board[row][i] == num:  #Check for conflicts in the same row
            board[row][col] = 0  #Revert the assignment
            return False
        if i != row and board[i][col] == num:  # Check for conflicts in the same column
            board[row][col] = 0  # Revert the assignment
            return False
    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and board[i][j] == num:  # Check for conflicts in the same 3x3 subgrid
                board[row][col] = 0  # Revert the assignment
                return False

    return True  # No conflicts found
def apply_arc_consistency(board): #reduce domain based on constraints
    queue = [] #
    domains = []  #domain of each cell
    domains = []

    domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)] # domain of cell that is empty

    steps = []  # List to store the steps of arc consistency

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                domains[i][j] = [board[i][j]] # domain for cell = its value
                queue.append((i, j)) # index of cell that have element

    def revise(xi, xj):
        revised = False
        removed_values = []
        for value in domains[xi[0]][xi[1]]: #index of neighbur  cell
            if isinstance(domains[xj[0]][xj[1]], list) and value in domains[xj[0]][xj[1]]:
                domains[xi[0]][xi[1]].remove(value)
                removed_values.append(value)
                revised = True
        if revised:
            steps.append(((xi[0], xi[1]), (xj[0], xj[1]), removed_values))
            print(f"Revised: {removed_values} removed from ({xi[0]}, {xi[1]})'s domain due to ({xj[0]}, {xj[1]})")
        return revised

    while queue:
        xi, xj = queue.pop(0) # compare two cells
        print(f"Processing cell ({xi}, {xj})")
        for i in range(9):
            if i != xi and revise((i, xj), (xi, xj)): # iterate every cell in same column
                if len(domains[i][xj]) == 0:
                    return None, steps
                queue.append((i, xj))
        for j in range(9):
            if j != xj and revise((xi, j), (xi, xj)): #iterate every row in same row
                if len(domains[xi][j]) == 0:
                    return None, steps
                queue.append((xi, j))

    return domains, steps

def solve_sudoku(initial_board):
    board = copy.deepcopy(initial_board)

    if not backtracking(board): #if backtracking false
        print("The puzzle is unsolvable.")
        return None

    domains, steps = apply_arc_consistency(board)
    if domains is None:
        print("Arc consistency failed. The puzzle might be unsolvable.")
        return None

    # Create a new board with resolved values
    solved_board = [[domains[i][j][0] if isinstance(domains[i][j], list) and len(domains[i][j]) == 1 else 0 for j in range(9)] for i in range(9)]

    return solved_board
def is_valid_sudoku(board):
    def is_valid_row(board, row):
        seen = set()
        for num in board[row]:
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def is_valid_column(board, col):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def is_valid_subgrid(board, start_row, start_col):
        seen = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = board[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)
        return True

    for i in range(9):
        if not is_valid_row(board, i) or not is_valid_column(board, i):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_valid_subgrid(board, i, j):
                return False

    return True


def is_initial_state_valid(board):
    if not is_valid_sudoku(board):
        print("The initial state of the Sudoku puzzle is not valid.")
        return False

    return True
def generate_random_puzzle():
    board = np.zeros((9, 9), dtype=int)  #9x9 zero board

    # Fill random places of the puzzle
    for _ in range(np.random.randint(12, 25)):  #Adjust the range for puzzle difficulty
        row, col, num = np.random.randint(9, size=3)
        while not is_valid_move(board, row, col, num + 1): #Checks if placing the selected number in the chosen position is a valid move
            row, col, num = np.random.randint(9, size=3) #If not, it continues to randomly select new positions until a valid move is found.
        board[row][col] = num + 1

    return board