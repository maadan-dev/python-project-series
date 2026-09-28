from validation import is_valid
from random import randint as random

def sudoku_generator(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if sudoku_generator(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def count_solutions(board):
    count = 0
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        count += count_solutions(board)
                        board[row][col] = 0
                return 0
    return 1

def remove_cells(board):
    solution_count = 0
    removal_count = 0

    while removal_count <= 45:

        i = random(0, 8)
        j =  random(0, 8)
        temp = 0
        if board[i][j] != 0:
            temp, board[i][j] = board[i][j], 0

            solution_count += count_solutions(board)

            if solution_count >= 2:
                board[i][j] = temp
            else:
                removal_count += 1
        solution_count = 0

