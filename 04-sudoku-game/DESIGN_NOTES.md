# Design Notes

This document describes the assumptions, promises, and current boundaries of the Sudoku Game application.

The purpose is to make the boundaries of the application explicit rather than assuming the code will handle situations it was not designed for.

## Assumptions

### Board Representation

* The board is represented as a 9×9 grid using a nested list of integers (`list[list[int]]`).
* Grid coordinates are zero-indexed, with rows and columns spanning from `0` to `8`.
* Empty cells are represented by `0`.
* Filled cells contain integer values from `1` to `9`.
* The 9×9 grid is divided into nine 3×3 subgrids (boxes), determined by integer division:
  ```python
  box_row = (row // 3) * 3
  box_col = (col // 3) * 3
  ```

### Data Types and Validation

* Row, column, and cell values can be passed as integers or numeric values/strings convertible via `int(val)`.
* Coordinate inputs are expected to be within the range `0` to `8`.
* Cell values are expected to be in the range `0` to `9` (where `0` denotes an empty cell).
* The `Board` class encapsulates grid state and coordinate validation.
* Pure logic functions in `generator.py` and `validation.py` operate on raw 9×9 nested lists (`board.board` or `list[list[int]]`), keeping game rules decoupled from UI dependencies.

### Puzzle Generation and Solving

* `sudoku_generator()` assumes it is given an empty 9×9 grid (all zeros) or a partially filled valid grid.
* Candidate digits (`1–9`) are shuffled at each empty cell, ensuring every generated board is uniquely randomized.
* `remove_cells()` assumes the input board is a completely filled, valid Sudoku grid before removing digits.
* Solvability is determined by `count_solutions()`, which searches for solutions and halts as soon as it detects `solutions >= 2`.

### Desktop Environment & UI

* The application runs locally as a desktop GUI using Flet (`flet==1.0.2`).
* User interaction is performed via keyboard (digit keys, arrows, Backspace/Delete, shortcuts) or mouse clicks on the grid and numpad controls.

## Promises

### Board Encapsulation (`board.py`)

`Board` promises that:

* `__init__()` initializes a 9×9 board with all cells set to `0`.
* `validate()` ensures an input is numeric and within given minimum and maximum bounds, converting numeric strings or raising a `ValueError` if invalid.
* `get_cell_value(row, col)` validates coordinates (`0–8`) and returns the cell's current value.
* `set_cell_value(row, col, val)` validates coordinates (`0–8`) and verifies that `val` is between `0` and `9` before updating the cell (allowing `0` to clear cells).
* `is_cell_empty(row, col)` validates coordinates and returns `True` if the cell contains `0`, and `False` otherwise.
* `reset_board()` resets all cells in `self.board` back to `0`.

### Rule Validation (`validation.py`)

* `is_valid(board, row, col, num)` verifies that placing `num` at `(row, col)` does not conflict with any other cell in the same row, column, or 3×3 subgrid. It explicitly skips comparing the cell against itself (`r != row or c != col`), preventing false conflicts when checking already-placed numbers.
* `is_board_solved(board)` verifies that no cells remain empty (`0`) and every cell satisfies Sudoku rules, returning `True` only when the board is completely and correctly solved.

### Puzzle Generation and Digging (`generator.py`)

* `sudoku_generator(board)` uses recursive backtracking with randomized candidate order (`shuffle(numbers)`) to fill all empty cells, returning `True` on success and mutating `board` in place.
* `count_solutions(board)` counts available solutions using an inner recursive search that short-circuits as soon as two solutions are discovered (`solutions >= 2`), returning `0`, `1`, or `2`.
* `remove_cells(board, target_empty=45)` randomly shuffles cell coordinates and removes numbers one by one, keeping each removal only if `count_solutions(board) == 1`. It halts when `target_empty` cells are removed or no more cells can be safely removed.

### User Interface and Interaction (`gui.py`)

`SudokuApp` promises that:

* The board renders an interactive 9×9 grid with visual distinction for 3×3 blocks, initial clue cells, player moves, conflicts, and matching-number highlights.
* Difficulty selection configures the puzzle generator:
  * **Easy**: ~32 empty cells
  * **Medium**: ~42 empty cells
  * **Hard**: ~50 empty cells
  * **Expert**: ~56 empty cells
* Move history is maintained on an in-memory stack, allowing single or multi-step undo (`Ctrl+Z` or Undo button).
* A hint solver identifies an empty cell and places its correct solution digit.
* A live game timer tracks elapsed time, supports pause and resume, and pauses when victory is achieved.
* Theme switching toggles between cohesive light and dark palettes.

## Will Not Handle

The current version intentionally does not handle:

### Persistence and Resumption

* Ongoing games are not saved to disk; closing the application window terminates the game and loses progress.
* Move history, timer states, and difficulty statistics are not persisted between runs.
* No save slots or autosave functionality.

### Custom Puzzle Import and Export

* Puzzles cannot be loaded from external files (JSON, CSV, SDK formats, or 81-character strings).
* Completed or in-progress games cannot be exported to print-friendly formats (PDF or images).

### Advanced Player Assistance

* No manual pencil marks / candidate notation system for intermediate solving.
* No explanatory solver (hints place the correct digit directly rather than explaining deduction logic like naked pairs or X-wings).
* No mistake limit / strikeout counter (mistakes are highlighted but do not trigger a game over).

### Multi-User and Networking

* CLI-only play is deprecated in favor of the Flet desktop GUI.
* No online multiplayer, shared leaderboards, or remote puzzle syncing.

## Design Decisions

### Separation of Logic and Presentation

All core Sudoku mechanics (`board.py`, `validation.py`, `generator.py`) contain zero GUI or Flet dependencies. They are pure Python modules that can be imported, tested, and verified independently of any graphical window.

```text
board.py       → Board state encapsulation & coordinate bounds checking
validation.py  → Pure Sudoku constraint checking (row, column, box, solved)
generator.py   → Randomized backtracking generator & unique solution digger
gui.py         → Flet desktop presentation, theme palette, event handlers, timer
main.py        → Application entry point
```

### Randomization with Candidate Shuffling

Instead of checking candidate digits `1–9` sequentially, `sudoku_generator()` shuffles candidate numbers for each empty cell:

```python
numbers = list(range(1, 10))
shuffle(numbers)
```

This guarantees every generated puzzle is different while retaining $O(1)$ constraint validation.

### Short-Circuit Solution Counting

To verify that a puzzle has exactly one solution, `count_solutions()` halts search recursion immediately when `solutions >= 2`:

```python
if solutions >= 2:
    return
```

This optimization eliminates unnecessary exhaustive tree exploration when verifying uniqueness during cell removal.

### Rebuilding Display from State

`gui.py` uses `update_board_visuals()` to synchronize the visual cells directly from the internal board state and selection models. This avoids fragile manual UI patching and ensures visual consistency across themes, undo operations, hints, and new games.

### In-Memory Undo Stack

Undo operations are tracked via a simple stack of move records:

```python
self.history.append((row, col, old_val, new_val))
```

Reverting a move pops the record from the stack and restores `old_val`, providing instantaneous and reliable undo without duplicating entire board matrices.

## Current Boundary

This project marks the transition in the Python project series from procedural logic and APIs into desktop GUI applications, algorithm design, and state management:

```text
Project 01 (Contact Book)       → Dictionaries, CRUD, JSON file persistence
Project 02 (Study Planner)      → External APIs, AI agent state, environment configuration
Project 03 (Invoice Generator)  → Data modeling, business calculations, PDF document generation
Project 04 (Sudoku Game)        → Matrix algorithms, constraint satisfaction, desktop GUI (Flet)
Project 05 (Invoice API)        → Modern REST APIs, web frameworks (FastAPI), backend services
```

The Sudoku game provides a complete desktop experience with robust puzzle generation, uniqueness verification, and responsive user controls. Future enhancements may explore save-state persistence and pencil marks, while the series progresses into web application programming.
