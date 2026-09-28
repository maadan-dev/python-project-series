def is_valid(board, row, col, num):
    for i in range(9):
        if board[i][col] == num or board[row][i] == num:
            return False

        box_row = (row // 3) * 3 + (i // 3)
        box_col = (col // 3) * 3 + (i % 3)
        if board[box_row][box_col] == num:
            return False

    return True
