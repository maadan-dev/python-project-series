
import flet as ft

from board import Board
from validation import is_valid, is_board_solved
from generator import sudoku_generator, remove_cells


class SudokuApp:
    # ── Color palette ───────────────────────────────────────
    BG_COLOR = "#F4F1FF"
    CARD_COLOR = "#FFFFFF"

    CELL_COLOR = "#FFFFFF"
    PREFILLED_COLOR = "#E9E3FF"

    BORDER_COLOR = "#DDD6FE"
    BOX_BORDER_COLOR = "#8B5CF6"

    TEXT_COLOR = "#29243A"
    PREFILLED_TEXT = "#5B21B6"
    USER_TEXT = "#2563EB"

    ACCENT_COLOR = "#7C3AED"
    ACCENT_HOVER = "#6D28D9"

    SUCCESS_COLOR = "#16A34A"
    ERROR_COLOR = "#EF4444"

    MUTED_COLOR = "#7C748F"

    def __init__(self, page: ft.Page, board: Board):
        self.page = page
        self.board = board

        # ── Page ────────────────────────────────────────────
        self.page.title = "Sudoku"
        self.page.bgcolor = self.BG_COLOR

        self.page.window.width = 540
        self.page.window.height = 760

        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # ── Cell references ────────────────────────────────
        self.text_fields = [
            [None for _ in range(9)]
            for _ in range(9)
        ]

    # ───────────────────────────────────────────────────────
    # GAME LOGIC
    # ───────────────────────────────────────────────────────

    def on_cell_input(self, e, row, col):
        value = e.control.value

        # Empty cell
        if value == "":
            self.board.set_cell_value(row, col, 0)
            e.control.text_style = ft.TextStyle(
                size=18,
                color=self.USER_TEXT,
            )
            return

        # Only allow numbers 1-9
        if not value.isdigit() or len(value) != 1 or value == "0":
            e.control.value = ""
            self.page.update()
            return

        value = int(value)

        try:
            self.board.set_cell_value(row, col, value)
        except ValueError:
            e.control.value = ""
            self.page.update()
            return

        # Invalid move
        if not is_valid(
            self.board.board,
            row,
            col,
            value,
        ):
            self.board.set_cell_value(row, col, 0)

            e.control.value = ""
            e.control.bgcolor = "#FEE2E2"

            self.page.update()

            # Return to normal after showing the error
            e.control.bgcolor = self.CELL_COLOR
            self.page.update()

            return

        # Valid user-entered number
        e.control.text_style = ft.TextStyle(
            size=18,
            weight=ft.FontWeight.BOLD,
            color=self.USER_TEXT,
        )

        # Puzzle solved
        if is_board_solved(self.board.board):
            self.page.show_dialog(
                ft.SnackBar(
                    content=ft.Text(
                        "🎉 Puzzle solved! Great job!",
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    bgcolor=self.SUCCESS_COLOR,
                )
            )

        self.page.update()

    def start_new_game(self, e):
        self.board.reset_board()

        sudoku_generator(self.board.board)
        remove_cells(self.board.board)

        for row in range(9):
            for col in range(9):
                value = self.board.get_cell_value(row, col)
                is_prefilled = value != 0

                cell = self.text_fields[row][col]

                cell.value = (
                    str(value)
                    if is_prefilled
                    else ""
                )

                cell.read_only = is_prefilled

                cell.text_style = ft.TextStyle(
                    size=18,
                    weight=(
                        ft.FontWeight.BOLD
                        if is_prefilled
                        else ft.FontWeight.NORMAL
                    ),
                    color=(
                        self.PREFILLED_TEXT
                        if is_prefilled
                        else self.USER_TEXT
                    ),
                )

                cell.bgcolor = (
                    self.PREFILLED_COLOR
                    if is_prefilled
                    else self.CELL_COLOR
                )

        self.page.update()

    # ───────────────────────────────────────────────────────
    # GRID
    # ───────────────────────────────────────────────────────

    def create_cell(self, row, col):
        value = self.board.get_cell_value(row, col)
        is_prefilled = value != 0

        # Thicker borders around the 3x3 boxes
        top = 2 if row % 3 == 0 else 1
        left = 2 if col % 3 == 0 else 1
        bottom = 2 if row == 8 else 1
        right = 2 if col == 8 or (col + 1) % 3 == 0 else 1

        cell = ft.TextField(
            value=str(value) if is_prefilled else "",

            width=47,
            height=47,

            text_align=ft.TextAlign.CENTER,

            text_style=ft.TextStyle(
                size=18,

                weight=(
                    ft.FontWeight.BOLD
                    if is_prefilled
                    else ft.FontWeight.NORMAL
                ),

                color=(
                    self.PREFILLED_TEXT
                    if is_prefilled
                    else self.USER_TEXT
                ),
            ),

            read_only=is_prefilled,

            bgcolor=(
                self.PREFILLED_COLOR
                if is_prefilled
                else self.CELL_COLOR
            ),

            border=ft.InputBorder.OUTLINE,

            border_color=(
                self.BOX_BORDER_COLOR
                if (
                    row % 3 == 0
                    or col % 3 == 0
                    or row == 8
                    or col == 8
                    or (col + 1) % 3 == 0
                )
                else self.BORDER_COLOR
            ),

            focused_border_color=self.ACCENT_COLOR,

            border_radius=6,

            content_padding=0,

            cursor_color=self.ACCENT_COLOR,

            on_change=lambda e, r=row, c=col:
                self.on_cell_input(e, r, c),
        )

        self.text_fields[row][col] = cell

        return cell

    def build_grid(self):
        rows = []

        for row in range(9):
            cells = []

            for col in range(9):
                cells.append(
                    self.create_cell(row, col)
                )

            rows.append(
                ft.Row(
                    controls=cells,
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        return ft.Column(
            controls=rows,
            spacing=2,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # ───────────────────────────────────────────────────────
    # HEADER
    # ───────────────────────────────────────────────────────

    def build_header(self):
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "9",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                            width=38,
                            height=38,
                            bgcolor=self.ACCENT_COLOR,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                        ),

                        ft.Text(
                            "Sudoku",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=self.TEXT_COLOR,
                        ),
                    ],

                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),

                ft.Text(
                    "Challenge your brain • One cell at a time",
                    size=13,
                    color=self.MUTED_COLOR,
                ),
            ],

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        )

    # ───────────────────────────────────────────────────────
    # BUTTON
    # ───────────────────────────────────────────────────────

    def build_new_game_button(self):
        return ft.Button(
            content="New Game",
            icon=ft.Icons.REFRESH,
            color="#FFFFFF",
            bgcolor=self.ACCENT_COLOR,
            on_click=self.start_new_game,
        )

    # ───────────────────────────────────────────────────────
    # MAIN UI
    # ───────────────────────────────────────────────────────

    def render(self):
        header = self.build_header()

        # Sudoku board
        grid = ft.Container(
            content=self.build_grid(),

            padding=16,

            bgcolor=self.CARD_COLOR,

            border=ft.Border.all(
                width=1,
                color=self.BORDER_COLOR,
            ),

            border_radius=18,

            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=2,
                offset=ft.Offset(0, 8),
                color="#22000000",
            ),
        )

        # Small legend
        legend = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=12,
                            height=12,
                            bgcolor=self.PREFILLED_COLOR,
                            border_radius=3,
                        ),
                        ft.Text(
                            "Given",
                            size=12,
                            color=self.MUTED_COLOR,
                        ),
                    ],
                    spacing=5,
                ),

                ft.Row(
                    controls=[
                        ft.Container(
                            width=12,
                            height=12,
                            bgcolor=self.CELL_COLOR,
                            border=ft.Border.all(
                                width=1,
                                color=self.BORDER_COLOR,
                            ),
                            border_radius=3,
                        ),
                        ft.Text(
                            "Your answer",
                            size=12,
                            color=self.MUTED_COLOR,
                        ),
                    ],
                    spacing=5,
                ),
            ],

            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        new_game_button = self.build_new_game_button()

        content = ft.Column(
            controls=[
                header,

                grid,

                legend,

                new_game_button,
            ],

            spacing=16,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Main card
        page_content = ft.Container(
            content=content,

            padding=24,

            bgcolor=self.CARD_COLOR,

            border_radius=24,

            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=4,
                offset=ft.Offset(0, 12),
                color="#18000000",
            ),
        )

        self.page.add(page_content)

        self.page.update()

