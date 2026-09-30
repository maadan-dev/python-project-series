import flet as ft
import time
import threading
from copy import deepcopy

from board import Board
from validation import is_valid, is_board_solved
from generator import sudoku_generator, remove_cells


def solve_board_matrix(board_matrix):
    """Solve a Sudoku board matrix using backtracking to get complete solution."""
    b = [row[:] for row in board_matrix]

    def backtrack():
        for r in range(9):
            for c in range(9):
                if b[r][c] == 0:
                    for n in range(1, 10):
                        if is_valid(b, r, c, n):
                            b[r][c] = n
                            if backtrack():
                                return True
                            b[r][c] = 0
                    return False
        return True

    if backtrack():
        return b
    return None


class Palette:
    def __init__(self, dark=False):
        self.dark = dark
        if dark:
            self.BG = "#0F172A"             # Slate 900
            self.CARD = "#1E293B"           # Slate 800
            self.CARD_BORDER = "#334155"    # Slate 700
            self.TEXT_PRIMARY = "#F8FAFC"   # White
            self.TEXT_SECONDARY = "#94A3B8" # Slate 400

            self.BLOCK_BG = "#0F172A"       # Dark block background
            self.BLOCK_BORDER = "#64748B"   # Slate 500 block border

            self.CELL_BG = "#1E293B"
            self.CELL_BORDER = "#475569"   # Crisp slate border for inner cells
            self.PREFILLED_BG = "#1E1B4B"    # Dark indigo tint
            self.PREFILLED_TEXT = "#A5B4FC"  # Light indigo
            self.USER_TEXT = "#38BDF8"       # Sky blue

            self.SELECTED_BG = "#6366F1"     # Indigo 500
            self.SELECTED_TEXT = "#FFFFFF"
            self.SELECTED_EMPTY_BG = "#312E81"# Soft dark indigo focus tint

            self.PEER_BG = "#2D3748"         # Soft dark guide
            self.SAME_NUM_BG = "#3730A3"     # Medium indigo highlight
            self.SAME_NUM_TEXT = "#FFFFFF"

            self.ERROR_BG = "#7F1D1D"        # Dark red
            self.ERROR_TEXT = "#FCA5A5"

            self.ACCENT = "#6366F1"
            self.ACCENT_HOVER = "#4F46E5"
            self.ACCENT_LIGHT = "#312E81"

            self.NUMPAD_BG = "#1E293B"
            self.NUMPAD_TEXT = "#F8FAFC"
            self.NUMPAD_BORDER = "#475569"
            self.BADGE_BG = "#312E81"
            self.BADGE_TEXT = "#C7D2FE"
        else:
            self.BG = "#F8FAFC"             # Slate 50
            self.CARD = "#FFFFFF"
            self.CARD_BORDER = "#CBD5E1"    # Slate 300
            self.TEXT_PRIMARY = "#0F172A"   # Slate 900
            self.TEXT_SECONDARY = "#475569" # Slate 600

            self.BLOCK_BG = "#E2E8F0"       # Slate 200 block gap separator
            self.BLOCK_BORDER = "#475569"   # Slate 600 box border

            self.CELL_BG = "#FFFFFF"
            self.CELL_BORDER = "#94A3B8"   # Crisp medium slate border for inner cells
            self.PREFILLED_BG = "#EEF2FF"    # Soft indigo given cell
            self.PREFILLED_TEXT = "#3730A3"  # Bold indigo text
            self.USER_TEXT = "#1D4ED8"       # Blue 700 user text

            self.SELECTED_BG = "#4F46E5"     # Vibrant Indigo 600
            self.SELECTED_TEXT = "#FFFFFF"
            self.SELECTED_EMPTY_BG = "#EEF2FF"# Soft indigo focus tint for empty cell

            self.PEER_BG = "#F1F5F9"         # Slate 100 guide
            self.SAME_NUM_BG = "#C7D2FE"     # Indigo 200 highlight
            self.SAME_NUM_TEXT = "#1E1B4B"

            self.ERROR_BG = "#FEE2E2"        # Red 100
            self.ERROR_TEXT = "#DC2626"      # Red 600

            self.ACCENT = "#4F46E5"
            self.ACCENT_HOVER = "#4338CA"
            self.ACCENT_LIGHT = "#EEF2FF"

            self.NUMPAD_BG = "#FFFFFF"
            self.NUMPAD_TEXT = "#0F172A"
            self.NUMPAD_BORDER = "#CBD5E1"
            self.BADGE_BG = "#EEF2FF"
            self.BADGE_TEXT = "#4338CA"


class SudokuApp:
    DIFFICULTIES = {
        "Easy": 32,
        "Medium": 44,
        "Hard": 52,
        "Expert": 58,
    }

    def __init__(self, page: ft.Page, board: Board):
        self.page = page
        self.board = board

        # App Theme & State
        self.is_dark_mode = False
        self.palette = Palette(dark=self.is_dark_mode)

        self.difficulty = "Medium"
        self.selected_cell = (0, 0)
        self.history = []  # List of tuples (row, col, old_val, new_val)
        self.mistakes = 0
        self.paused = False

        # Solution cache for hints and validation
        self.solution = solve_board_matrix(self.board.board)
        self.is_prefilled = [
            [self.board.get_cell_value(r, c) != 0 for c in range(9)]
            for r in range(9)
        ]

        # Timer setup
        self.start_time = time.time()
        self.elapsed_seconds = 0
        self.timer_running = True
        self.timer_thread = None

        # Control References
        self.cell_containers = [[None for _ in range(9)] for _ in range(9)]
        self.cell_texts = [[None for _ in range(9)] for _ in range(9)]
        self.numpad_buttons = {}
        self.numpad_badges = {}

        self.diff_text = None
        self.timer_text = None
        self.mistakes_text = None
        self.remaining_text = None

        # Configure Page
        self.page.title = "Sudoku Master"
        self.page.bgcolor = self.palette.BG
        self.page.window.width = 560
        self.page.window.height = 880
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        # Keyboard Listener
        self.page.on_keyboard_event = self.on_key_press

    # ───────────────────────────────────────────────────────
    # TIMER CONTROL
    # ───────────────────────────────────────────────────────

    def start_timer(self):
        self.timer_running = True

        def run():
            while self.timer_running:
                time.sleep(1)
                if not self.paused and self.timer_running:
                    self.elapsed_seconds += 1
                    if self.timer_text:
                        mins, secs = divmod(self.elapsed_seconds, 60)
                        self.timer_text.value = f"{mins:02d}:{secs:02d}"
                        self.page.update()

        self.timer_thread = threading.Thread(target=run, daemon=True)
        self.timer_thread.start()

    def toggle_pause(self, e=None):
        self.paused = not self.paused
        if self.paused:
            self.show_snack("Game Paused", self.palette.ACCENT)
        else:
            self.show_snack("Game Resumed", self.palette.ACCENT)
        self.update_board_visuals()

    # ───────────────────────────────────────────────────────
    # GAMEPLAY LOGIC
    # ───────────────────────────────────────────────────────

    def select_cell(self, row, col):
        if self.paused:
            return
        self.selected_cell = (row, col)
        self.update_board_visuals()

    def on_key_press(self, e: ft.KeyboardEvent):
        if self.paused or not self.selected_cell:
            return

        row, col = self.selected_cell

        # Arrow key navigation
        if e.key == "ArrowUp":
            self.selected_cell = (max(0, row - 1), col)
            self.update_board_visuals()
            return
        elif e.key == "ArrowDown":
            self.selected_cell = (min(8, row + 1), col)
            self.update_board_visuals()
            return
        elif e.key == "ArrowLeft":
            self.selected_cell = (row, max(0, col - 1))
            self.update_board_visuals()
            return
        elif e.key == "ArrowRight":
            self.selected_cell = (row, min(8, col + 1))
            self.update_board_visuals()
            return

        # Number input
        if e.key in "123456789":
            self.input_number(int(e.key))
        elif e.key in ("Backspace", "Delete", "0"):
            self.erase_cell()
        elif (e.ctrl or e.meta) and e.key.lower() == "z":
            self.undo_move()

    def input_number(self, num: int):
        if self.paused or not self.selected_cell:
            return

        row, col = self.selected_cell

        # Cannot edit prefilled cells
        if self.is_prefilled[row][col]:
            self.show_snack("Given clues cannot be changed", self.palette.TEXT_SECONDARY)
            return

        curr_val = self.board.get_cell_value(row, col)
        if curr_val == num:
            return

        # Validate entry
        if not is_valid(self.board.board, row, col, num):
            self.mistakes += 1
            if self.mistakes_text:
                self.mistakes_text.value = f"Mistakes: {self.mistakes}"

            # Visual conflict alert on cell
            self.cell_containers[row][col].bgcolor = self.palette.ERROR_BG
            self.cell_texts[row][col].color = self.palette.ERROR_TEXT
            self.cell_texts[row][col].value = str(num)
            self.show_snack(f"Conflict: {num} already in row, column, or 3x3 box!", self.palette.ERROR_BG)
            self.page.update()
            return

        # Record move into history
        self.history.append((row, col, curr_val, num))
        self.board.set_cell_value(row, col, num)

        self.update_board_visuals()

        # Check completion
        if is_board_solved(self.board.board):
            self.handle_victory()

    def erase_cell(self, e=None):
        if self.paused or not self.selected_cell:
            return

        row, col = self.selected_cell
        if self.is_prefilled[row][col]:
            self.show_snack("Given clues cannot be erased", self.palette.TEXT_SECONDARY)
            return

        curr_val = self.board.get_cell_value(row, col)
        if curr_val == 0:
            return

        self.history.append((row, col, curr_val, 0))
        self.board.set_cell_value(row, col, 0)
        self.update_board_visuals()

    def undo_move(self, e=None):
        if self.paused or not self.history:
            self.show_snack("Nothing to undo", self.palette.TEXT_SECONDARY)
            return

        row, col, old_val, new_val = self.history.pop()
        self.board.set_cell_value(row, col, old_val)
        self.selected_cell = (row, col)
        self.update_board_visuals()

    def give_hint(self, e=None):
        if self.paused:
            return

        if not self.solution:
            self.solution = solve_board_matrix(self.board.board)

        if not self.solution:
            self.show_snack("No valid solution found for current board!", self.palette.ERROR_BG)
            return

        row, col = self.selected_cell if self.selected_cell else (None, None)
        target = None

        if row is not None and col is not None and not self.is_prefilled[row][col] and self.board.get_cell_value(row, col) == 0:
            target = (row, col)
        else:
            for r in range(9):
                for c in range(9):
                    if self.board.get_cell_value(r, c) == 0:
                        target = (r, c)
                        break
                if target:
                    break

        if not target:
            self.show_snack("Board is already complete!", self.palette.ACCENT)
            return

        r, c = target
        correct_val = self.solution[r][c]
        self.history.append((r, c, self.board.get_cell_value(r, c), correct_val))
        self.board.set_cell_value(r, c, correct_val)
        self.selected_cell = (r, c)
        self.show_snack(f"Hint: Placed {correct_val} at cell ({r+1}, {c+1})", self.palette.ACCENT)
        self.update_board_visuals()

        if is_board_solved(self.board.board):
            self.handle_victory()

    def handle_victory(self):
        mins, secs = divmod(self.elapsed_seconds, 60)
        time_str = f"{mins:02d}:{secs:02d}"

        def close_dialog(e):
            self.page.pop_dialog()
            self.start_new_game()

        dialog = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, color="#EAB308", size=32),
                    ft.Text("Puzzle Solved!", weight=ft.FontWeight.BOLD, size=22, color=self.palette.TEXT_PRIMARY),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            content=ft.Column(
                controls=[
                    ft.Text(f"🎉 Fantastic job! You solved the puzzle.", color=self.palette.TEXT_PRIMARY, size=15),
                    ft.Container(height=10),
                    ft.Row(
                        controls=[
                            ft.Text(f"⏱️ Time: {time_str}", weight=ft.FontWeight.BOLD, color=self.palette.ACCENT),
                            ft.Text(f"⚡ Difficulty: {self.difficulty}", weight=ft.FontWeight.BOLD, color=self.palette.TEXT_SECONDARY),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                    ft.Text(f"❌ Mistakes made: {self.mistakes}", color=self.palette.TEXT_SECONDARY, size=13),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
            ),
            actions=[
                ft.Button(
                    content="Play Again",
                    icon=ft.Icons.REFRESH_ROUNDED,
                    bgcolor=self.palette.ACCENT,
                    color="#FFFFFF",
                    on_click=close_dialog,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.show_dialog(dialog)

    def start_new_game(self, e=None):
        self.board.reset_board()
        sudoku_generator(self.board.board)
        target_empty = self.DIFFICULTIES.get(self.difficulty, 44)
        remove_cells(self.board.board, target_empty=target_empty)

        self.solution = solve_board_matrix(self.board.board)
        self.is_prefilled = [
            [self.board.get_cell_value(r, c) != 0 for c in range(9)]
            for r in range(9)
        ]
        self.history.clear()
        self.mistakes = 0
        self.elapsed_seconds = 0
        self.paused = False
        self.selected_cell = (0, 0)

        if self.mistakes_text:
            self.mistakes_text.value = "Mistakes: 0"
        if self.diff_text:
            self.diff_text.value = self.difficulty

        self.update_board_visuals()
        self.show_snack(f"New {self.difficulty} game started!", self.palette.ACCENT)

    def change_difficulty(self, diff_name: str):
        self.difficulty = diff_name
        self.start_new_game()

    def toggle_theme(self, e=None):
        self.is_dark_mode = not self.is_dark_mode
        self.palette = Palette(dark=self.is_dark_mode)
        self.page.bgcolor = self.palette.BG

        self.page.controls.clear()
        self.render()

    def show_snack(self, message: str, color: str):
        snack = ft.SnackBar(
            content=ft.Text(message, color="#FFFFFF", weight=ft.FontWeight.BOLD),
            bgcolor=color,
            duration=2000,
        )
        self.page.show_dialog(snack)

    # ───────────────────────────────────────────────────────
    # VISUAL UPDATES
    # ───────────────────────────────────────────────────────

    def update_board_visuals(self):
        sel_r, sel_c = self.selected_cell if self.selected_cell else (-1, -1)
        sel_val = self.board.get_cell_value(sel_r, sel_c) if sel_r >= 0 and sel_c >= 0 else 0

        counts = {n: 0 for n in range(1, 10)}
        empty_count = 0

        for r in range(9):
            for c in range(9):
                val = self.board.get_cell_value(r, c)
                if val in counts:
                    counts[val] += 1
                else:
                    empty_count += 1

                container = self.cell_containers[r][c]
                txt = self.cell_texts[r][c]

                if not container or not txt:
                    continue

                if self.paused:
                    txt.value = "?"
                    txt.color = self.palette.TEXT_SECONDARY
                    container.bgcolor = self.palette.CELL_BG
                    container.border = ft.Border.all(width=1, color=self.palette.CELL_BORDER)
                    continue

                txt.value = str(val) if val != 0 else ""
                is_given = self.is_prefilled[r][c]

                is_selected = (r == sel_r and c == sel_c)
                is_peer = (r == sel_r or c == sel_c or (r // 3 == sel_r // 3 and c // 3 == sel_c // 3))
                is_same_num = (sel_val > 0 and val == sel_val)

                if is_selected:
                    if val != 0:
                        container.bgcolor = self.palette.SELECTED_BG
                        txt.color = self.palette.SELECTED_TEXT
                        txt.weight = ft.FontWeight.BOLD
                    else:
                        container.bgcolor = self.palette.SELECTED_EMPTY_BG
                        txt.color = self.palette.USER_TEXT
                        txt.weight = ft.FontWeight.BOLD
                    container.border = ft.Border.all(width=2.5, color=self.palette.ACCENT)
                elif is_same_num:
                    container.bgcolor = self.palette.SAME_NUM_BG
                    txt.color = self.palette.SAME_NUM_TEXT
                    txt.weight = ft.FontWeight.BOLD
                    container.border = ft.Border.all(width=1.5, color=self.palette.ACCENT)
                elif is_peer:
                    container.bgcolor = self.palette.PEER_BG
                    txt.color = self.palette.PREFILLED_TEXT if is_given else self.palette.USER_TEXT
                    txt.weight = ft.FontWeight.BOLD if is_given else ft.FontWeight.NORMAL
                    container.border = ft.Border.all(width=1, color=self.palette.CELL_BORDER)
                elif is_given:
                    container.bgcolor = self.palette.PREFILLED_BG
                    txt.color = self.palette.PREFILLED_TEXT
                    txt.weight = ft.FontWeight.BOLD
                    container.border = ft.Border.all(width=1, color=self.palette.CELL_BORDER)
                else:
                    container.bgcolor = self.palette.CELL_BG
                    txt.color = self.palette.USER_TEXT
                    txt.weight = ft.FontWeight.BOLD
                    container.border = ft.Border.all(width=1, color=self.palette.CELL_BORDER)

        if self.remaining_text:
            self.remaining_text.value = f"Remaining: {empty_count}"

        for num in range(1, 10):
            rem = 9 - counts[num]
            if num in self.numpad_badges:
                badge = self.numpad_badges[num]
                btn = self.numpad_buttons[num]
                if rem <= 0:
                    badge.value = "✓"
                    badge.color = self.palette.ACCENT
                    btn.opacity = 0.5
                else:
                    badge.value = f"{rem}"
                    badge.color = self.palette.BADGE_TEXT
                    btn.opacity = 1.0

        self.page.update()

    # ───────────────────────────────────────────────────────
    # UI BUILDERS
    # ───────────────────────────────────────────────────────

    def build_header(self):
        theme_icon = ft.Icons.LIGHT_MODE_OUTLINED if self.is_dark_mode else ft.Icons.DARK_MODE_OUTLINED

        self.diff_text = ft.Text(
            self.difficulty,
            size=13,
            weight=ft.FontWeight.BOLD,
            color=self.palette.TEXT_PRIMARY,
        )

        diff_menu = ft.PopupMenuButton(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        self.diff_text,
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN_ROUNDED, size=18, color=self.palette.TEXT_PRIMARY),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                bgcolor=self.palette.BLOCK_BG,
                border=ft.Border.all(width=1, color=self.palette.CARD_BORDER),
                border_radius=8,
            ),
            items=[
                ft.PopupMenuItem(
                    content=ft.Text("Easy", color=self.palette.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    on_click=lambda e: self.change_difficulty("Easy"),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Medium", color=self.palette.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    on_click=lambda e: self.change_difficulty("Medium"),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Hard", color=self.palette.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    on_click=lambda e: self.change_difficulty("Hard"),
                ),
                ft.PopupMenuItem(
                    content=ft.Text("Expert", color=self.palette.TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                    on_click=lambda e: self.change_difficulty("Expert"),
                ),
            ],
        )

        theme_btn = ft.IconButton(
            icon=theme_icon,
            icon_color=self.palette.TEXT_PRIMARY,
            tooltip="Toggle Light/Dark Theme",
            on_click=self.toggle_theme,
        )

        self.timer_text = ft.Text(
            "00:00",
            size=15,
            weight=ft.FontWeight.BOLD,
            color=self.palette.TEXT_PRIMARY,
        )

        pause_btn = ft.IconButton(
            icon=ft.Icons.PAUSE_ROUNDED if not self.paused else ft.Icons.PLAY_ARROW_ROUNDED,
            icon_color=self.palette.ACCENT,
            tooltip="Pause/Resume",
            on_click=self.toggle_pause,
        )

        timer_box = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.TIMER_OUTLINED, size=18, color=self.palette.ACCENT),
                    self.timer_text,
                    pause_btn,
                ],
                spacing=4,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            bgcolor=self.palette.BLOCK_BG,
            border_radius=12,
            border=ft.Border.all(width=1, color=self.palette.CARD_BORDER),
        )

        top_row = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "9",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                            width=38,
                            height=38,
                            bgcolor=self.palette.ACCENT,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(
                            "Sudoku",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=self.palette.TEXT_PRIMARY,
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        diff_menu,
                        timer_box,
                        theme_btn,
                    ],
                    spacing=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return top_row

    def build_stats_bar(self):
        self.mistakes_text = ft.Text(
            f"Mistakes: {self.mistakes}",
            size=13,
            weight=ft.FontWeight.W_500,
            color=self.palette.TEXT_SECONDARY,
        )

        self.remaining_text = ft.Text(
            "Remaining: --",
            size=13,
            weight=ft.FontWeight.W_500,
            color=self.palette.TEXT_SECONDARY,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=16, color=self.palette.TEXT_SECONDARY),
                            self.mistakes_text,
                        ],
                        spacing=4,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=16, color=self.palette.TEXT_SECONDARY),
                            self.remaining_text,
                        ],
                        spacing=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
            bgcolor=self.palette.BLOCK_BG,
            border_radius=10,
        )

    def create_cell(self, row, col):
        txt = ft.Text(
            "",
            size=18,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        container = ft.Container(
            content=txt,
            width=43,
            height=43,
            alignment=ft.Alignment.CENTER,
            border_radius=6,
            bgcolor=self.palette.CELL_BG,
            border=ft.Border.all(width=1, color=self.palette.CELL_BORDER),
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            ink=True,
            on_click=lambda e, r=row, c=col: self.select_cell(r, c),
        )

        self.cell_containers[row][col] = container
        self.cell_texts[row][col] = txt

        return container

    def build_grid(self):
        block_rows = []

        for b_r in range(3):
            block_cols = []
            for b_c in range(3):
                cell_rows = []
                for r_in_b in range(3):
                    r = b_r * 3 + r_in_b
                    cell_cols = []
                    for c_in_b in range(3):
                        c = b_c * 3 + c_in_b
                        cell_cols.append(self.create_cell(r, c))
                    cell_rows.append(
                        ft.Row(
                            controls=cell_cols,
                            spacing=2,
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    )

                block_container = ft.Container(
                    content=ft.Column(
                        controls=cell_rows,
                        spacing=2,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=4,
                    border=ft.Border.all(width=2, color=self.palette.BLOCK_BORDER),
                    border_radius=10,
                    bgcolor=self.palette.BLOCK_BG,
                )
                block_cols.append(block_container)

            block_rows.append(
                ft.Row(
                    controls=block_cols,
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        return ft.Column(
            controls=block_rows,
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def build_action_bar(self):
        def make_action_btn(icon, label, callback):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(icon, size=20, color=self.palette.ACCENT),
                        ft.Text(label, size=11, weight=ft.FontWeight.W_500, color=self.palette.TEXT_PRIMARY),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=68,
                height=52,
                border_radius=10,
                bgcolor=self.palette.BLOCK_BG,
                border=ft.Border.all(width=1, color=self.palette.CARD_BORDER),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=callback,
            )

        return ft.Row(
            controls=[
                make_action_btn(ft.Icons.UNDO_ROUNDED, "Undo", self.undo_move),
                make_action_btn(ft.Icons.BACKSPACE_OUTLINED, "Erase", self.erase_cell),
                make_action_btn(ft.Icons.LIGHTBULB_OUTLINE, "Hint", self.give_hint),
                make_action_btn(ft.Icons.REFRESH_ROUNDED, "New Game", self.start_new_game),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

    def build_numpad(self):
        buttons = []

        for num in range(1, 10):
            badge = ft.Text(
                "9",
                size=10,
                weight=ft.FontWeight.BOLD,
                color=self.palette.BADGE_TEXT,
            )
            self.numpad_badges[num] = badge

            btn_content = ft.Column(
                controls=[
                    ft.Text(
                        str(num),
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self.palette.NUMPAD_TEXT,
                    ),
                    badge,
                ],
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )

            btn = ft.Container(
                content=btn_content,
                width=45,
                height=56,
                border_radius=10,
                bgcolor=self.palette.NUMPAD_BG,
                border=ft.Border.all(width=1, color=self.palette.NUMPAD_BORDER),
                alignment=ft.Alignment.CENTER,
                animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                ink=True,
                on_click=lambda e, n=num: self.input_number(n),
            )

            self.numpad_buttons[num] = btn
            buttons.append(btn)

        return ft.Row(
            controls=buttons,
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # ───────────────────────────────────────────────────────
    # MAIN UI RENDER
    # ───────────────────────────────────────────────────────

    def render(self):
        header = self.build_header()
        stats = self.build_stats_bar()
        grid = self.build_grid()
        actions = self.build_action_bar()
        numpad = self.build_numpad()

        card_content = ft.Column(
            controls=[
                header,
                stats,
                ft.Container(
                    content=grid,
                    padding=10,
                    bgcolor=self.palette.CARD,
                    border=ft.Border.all(width=1, color=self.palette.CARD_BORDER),
                    border_radius=16,
                    shadow=ft.BoxShadow(
                        blur_radius=20,
                        spread_radius=1,
                        offset=ft.Offset(0, 6),
                        color="#10000000",
                    ),
                ),
                actions,
                numpad,
            ],
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        main_card = ft.Container(
            content=card_content,
            width=500,
            padding=20,
            bgcolor=self.palette.CARD,
            border_radius=24,
            border=ft.Border.all(width=1, color=self.palette.CARD_BORDER),
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=2,
                offset=ft.Offset(0, 10),
                color="#18000000",
            ),
        )

        self.page.add(main_card)
        self.update_board_visuals()

        if not self.timer_thread:
            self.start_timer()
