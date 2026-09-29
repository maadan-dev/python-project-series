from board import Board
from generator import sudoku_generator, remove_cells
from gui import SudokuApp
import flet as ft

board = Board()
sudoku_generator(board.board)
remove_cells(board.board)

def main(page: ft.Page):
    app = SudokuApp(page, board)
    app.render()

if __name__ == "__main__":
    ft.run(main)