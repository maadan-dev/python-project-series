class Board: 
    def __init__(self): 
        self.board = [[0] * 9 for _ in range(9)] 
        
    def validate(self, val, min_val=0, max_val=8):
        try: 
            val = int(val) 
        except (ValueError, TypeError): 
            raise ValueError("Input must be a number") 
            
        if val < min_val or val > max_val: 
            raise ValueError(f"Input must be in range {min_val + 1}-{max_val + 1}") 
        return val 

    def get_cell_value(self, row, col):
        a = self.validate(row) 
        b = self.validate(col) 
        return self.board[a][b] 

    def set_cell_value(self, row, col, val):
        a = self.validate(row) 
        b = self.validate(col) 
        c = self.validate(val, min_val=1, max_val=9)  # Values are 1-9
        self.board[a][b] = c 

    def is_cell_empty(self, row, col):
        row = self.validate(row)
        col = self.validate(col)
        return self.board[row][col] == 0
        
    def reset_board(self):
        self.board = [[0] * 9 for _ in range(9)] 
