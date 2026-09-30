# Sudoku Master — Graphical Sudoku Game

A modern, interactive Sudoku game built with Python and Flet.

This is the fourth project in my Python project series. Unlike the previous CLI projects, this one introduced a graphical interface, recursion, backtracking, puzzle generation, solution counting, state-driven rendering, and event-driven programming.

The project lives inside the [python-project-series](https://github.com/maadan-dev/python-project-series) repository alongside the other projects in the series.

---

## What the Project Does

A feature-rich Sudoku application with a clean, responsive graphical interface that:

* **Generates Valid Sudoku Puzzles**: Generates a complete valid Sudoku board using recursive backtracking.
* **Preserves Unique Solutions**: Removes cells based on selected difficulty while ensuring only one unique solution exists.
* **Multiple Difficulty Levels**: Supports **Easy**, **Medium**, **Hard**, and **Expert** difficulty modes.
* **3×3 Subgrid Board Layout**: Displays the 9×9 grid visually partitioned into nine distinct 3×3 subgrid blocks.
* **Smart Cell Highlighting**: 
  * Selected cell focus with thick accent border.
  * Soft guide highlighting for the active cell's row, column, and 3×3 block.
  * Automatic matching-number highlighting across the entire board.
* **Live Timer & Pause**: Features a live stopwatch timer with pause/resume functionality.
* **Action Toolbar**:
  * **Undo**: Reverts moves using a history stack.
  * **Erase**: Clears user entries on editable cells.
  * **Hint**: Intelligently reveals the correct number for the selected cell or first empty cell using the solver.
  * **New Game**: Generates a fresh puzzle instantly.
* **Interactive Number Pad**: 1–9 digit buttons with remaining count badges (e.g., `4 left`, `✓` when completed).
* **Keyboard Navigation & Controls**:
  * Number keys `1`–`9` to enter values.
  * `Backspace` / `Delete` to clear.
  * Arrow keys (`ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`) to navigate the board.
  * Shortcuts (`Ctrl+Z` for Undo, `h` for Hint, `n` for New Game).
* **Light & Dark Theme Toggle**: Dynamic theme switching for comfortable play in any environment.
* **Victory Celebration**: Displays a celebratory modal dialog with final stats (time, difficulty, mistake count) upon solving the board.

---

## How to Run It

1. **Clone the main project repository:**
   ```bash
   git clone https://github.com/maadan-dev/python-project-series.git
   ```

2. **Enter the Sudoku project directory:**
   ```bash
   cd python-project-series/04-sudoku-game
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   ```
   * **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```
   * **Windows:**
     ```cmd
     .venv\Scripts\activate
     ```

4. **Install the project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the game:**
   ```bash
   python main.py
   ```

---

## Requirements

* `flet==1.0.2`
* Python 3.x is required.

---

## Project Structure

```text
04-sudoku-game/
├── board.py         # Board state encapsulation & validation
├── generator.py     # Recursive Sudoku generator & unique solution solver
├── gui.py           # Flet GUI application, theme palette, & event handlers
├── main.py          # Application entry point
├── validation.py     # Core Sudoku rules & completion checking
├── requirements.txt # Project dependencies (Flet 1.0.2)
└── README.md        # Project documentation
```

### Module Responsibilities

* **`board.py`**: Responsible for the 9×9 Sudoku board state, row/column index validation, cell getters/setters, empty cell checks, and board resetting.
* **`validation.py`**: Implements pure Sudoku rule checking for rows, columns, and 3×3 boxes, as well as verifying whether the entire board is completely and correctly solved.
* **`generator.py`**: Handles puzzle generation using recursive backtracking with randomized candidates, solution counting (`count_solutions`), and cell removal to guarantee a unique puzzle solution.
* **`gui.py`**: Implements the Flet graphical interface (`SudokuApp`), theme palette management (`Palette`), grid layout construction, cell selection logic, visual highlighting, action handlers (Undo, Erase, Hint), numpad, timer, and keyboard shortcuts.
* **`main.py`**: The application entry point. Initializes the board, generates the starting puzzle, creates the `SudokuApp`, and launches Flet via `ft.run(main)`.

---

## What I Learned

* How to structure a larger Python project across multiple files with separated responsibilities (board state, validation, generation, UI, application startup).
* How to represent and manipulate 2D matrix grids using nested Python lists.
* How classes encapsulate state and methods belonging to an object (`Board`, `SudokuApp`, `Palette`).
* How recursive backtracking algorithms work by trying values, making recursive calls, and unwinding state when a branch fails.
* How to count total solutions recursively to ensure puzzle uniqueness.
* How to separate core game logic from UI rendering using a "Single Source of Truth" design pattern (`update_board_visuals`).
* How event-driven programming works in Flet, including click events, dropdown/popup selection, and keyboard event listeners (`on_keyboard_event`).
* How stack-based history (`list.append` and `list.pop`) enables clean Undo functionality.
* How color palettes, subgrid borders, typography, spacing, and animations transform functional code into a polished application.

---

## What I Struggled With and How I Fixed It

1. **Closure Bug in Callbacks**:
   * *Problem:* I didn't initially understand why the grid callback used `lambda e, r=row, c=col: ...` instead of referencing `row` and `col` directly.
   * *Fix:* Learned how Python closures capture variables by reference and why loop variables must be bound as default arguments when creating callbacks dynamically in loops.

2. **Recursive Solution Counter**:
   * *Problem:* I struggled to see how `count_solutions()` accumulated solution counts through recursive branches.
   * *Fix:* Traced execution trees step-by-step to understand how each recursive branch contributes to the total count before returning.

3. **Scope and `reset_board()`**:
   * *Problem:* Reassigned a local variable inside `reset_board()` instead of mutating the object's actual state.
   * *Fix:* Paid close attention to mutating object attributes versus reassigning local variable names.

4. **Type Confusion (`Board` vs 2D List)**:
   * *Problem:* Repeatedly passed the `Board` object to functions expecting a raw 2D list (`board.board`).
   * *Fix:* Adopted the practice of explicitly checking variable types flowing into every function.

5. **`is_board_solved()` False Negatives**:
   * *Problem:* Validation logic caused the cell currently being checked to report a conflict with itself.
   * *Fix:* Ensured validation logic skips matching cell coordinates `(r != row or c != col)`.

6. **Flet Event Wiring & API Compatibility**:
   * *Problem:* Ran into argument mismatch issues on event callbacks (e.g. `on_select` vs `on_change` in Flet 1.0.2).
   * *Fix:* Inspected framework method signatures and aligned callback parameters with event payloads.

---

## Concepts Practiced

* Python OOP & Class Architecture
* Object State & Encapsulation
* 2D Matrix Grid Manipulation
* Scope & Closures (`lambda` default arguments)
* Recursive Backtracking Algorithms
* Solution Counting & Uniqueness Verification
* Exception Handling & Type Conversion
* Event-Driven GUI Programming with Flet 1.0.2
* Keyboard Event Listening (`on_keyboard_event`)
* Undo History Stack (`append` / `pop`)
* Theme Palette Management (Light/Dark Mode)
* State Synchronization & Visual Highlighting

---

## Status

This is a learning project built as part of my Python Project Series to master key programming concepts while creating a fully playable application.

---

## Part of the Python Project Series

This project is **Project 4** in my Python project series. The series tracks my progression from CLI utilities to full GUI and API applications.

👉 [View the full Python Project Series](https://github.com/maadan-dev/python-project-series)

---

## What's Next?

**Project 5 — Invoice API**  
Next up: turning invoice generation concepts into a backend API.  
→ [Project 5 — Invoice API](https://github.com/maadan-dev/python-project-series/05-invoice-api)
