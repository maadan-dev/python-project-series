def is_valid(board, row, col, num):
    for i in range(9):
        # Skip checking the cell against itself
        if i != col and board[row][i] == num:
            return False
        if i != row and board[i][col] == num:
            return False

        box_row = (row // 3) * 3 + (i // 3)
        box_col = (col // 3) * 3 + (i % 3)
        # Skip checking the cell against itself in the 3x3 box
        if (box_row != row or box_col != col) and board[box_row][box_col] == num:
            return False

    return True

def is_board_solved(board):
    for i in range(9):
        for j in range(9):
            val = board[i][j]
            if val == 0:  
                return False
            board[i][j] = 0
            if not is_valid(board, i, j, val):
                board[i][j] = val
                return False
            board[i][j] = val    
    return True