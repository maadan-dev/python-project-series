def is_valid(board, row, col, num):
    """
    Check whether placing num at board[row][col]
    would be valid according to Sudoku rules.
    """

    # Check row
    for c in range(9):
        if c != col and board[row][c] == num:
            return False

    # Check column
    for r in range(9):
        if r != row and board[r][col] == num:
            return False

    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r != row or c != col) and board[r][c] == num:
                return False

    return True


def is_board_solved(board):
    """
    Return True if every cell is filled and the entire
    board satisfies Sudoku rules.
    """

    for row in range(9):
        for col in range(9):
            value = board[row][col]

            if value == 0:
                return False

            if not is_valid(board, row, col, value):
                return False

    return True
