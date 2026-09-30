# Python Project Series

Small Python projects built one after another during the Learn2Earn AI Engineering Fellowship. Each one adds a concept the previous ones didn't cover, and each has its own README with setup steps, what I learned, and what broke.

Writeup and timeline: [maadan.dev/fellowship](https://maadan.dev/fellowship)

## Projects

| # | Project | What it is | New concepts |
|---|---------|------------|--------------|
| 01 | [Contact Book](01-contact-book) | CLI contact manager | dicts, JSON persistence, validation, CRUD |
| 02 | [Study Planner](02-study-planner) | Chat agent using Groq | LLM API calls, chat history, env secrets |
| 03 | [Invoice Generator](03-invoice-generator) | CLI invoices with PDF export | classes, serialization, ReportLab |
| 04 | [Sudoku](04-sudoku-game) | Desktop game (Flet) | recursion, backtracking, GUI, event handling |
| 05 | Invoice API | planned | backend API |

## Running a project

Every project is self-contained. Open its folder and follow its README. Each uses its own virtual environment.

```bash
git clone https://github.com/maadan-dev/python-project-series.git
cd python-project-series/<project-folder>
```

## Pattern across the projects

Most bugs weren't syntax. They came down to three questions: who owns the state, what type a value actually is, and when something runs. From project 5 on I'm adding type hints and checking them with `pyright`.
