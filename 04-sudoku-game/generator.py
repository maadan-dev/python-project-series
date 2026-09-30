
from random import randint, shuffle

from validation import is_valid


def sudoku_generator(board):
    """
    Generate a complete valid Sudoku board using backtracking.
    Candidate numbers are shuffled so each generated board
    is different.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                shuffle(numbers)

                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        if sudoku_generator(board):
                            return True

                        board[row][col] = 0

                return False

    return True


def remove_cells(board, target_empty=45):
    """
    Remove cells while keeping the puzzle uniquely solvable.

    Stops when:
    - target_empty cells have been removed, or
    - no more cells can be removed without creating
      multiple solutions.
    """
    removed = 0
    cells = [
        (row, col)
        for row in range(9)
        for col in range(9)
    ]

    shuffle(cells)

    for row, col in cells:
        if removed >= target_empty:
            break

        value = board[row][col]

        if value == 0:
            continue

        board[row][col] = 0

        if count_solutions(board) == 1:
            removed += 1
        else:
            board[row][col] = value

    return removed


def count_solutions(board):
    """
    Count Sudoku solutions, stopping as soon as two are found.

    Returns:
        0 -> no solution
        1 -> exactly one solution
        2 -> two or more solutions
    """
    solutions = 0

    def solve():
        nonlocal solutions

        if solutions >= 2:
            return

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num

                            solve()

                            board[row][col] = 0

                            if solutions >= 2:
                                return

                    return

        solutions += 1

    solve()

    return solutions
