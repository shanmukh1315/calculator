# Calculator (CLI) — Assignment

[![CI – Tests & Coverage](https://github.com/shanmukh1315/calculator/actions/workflows/python-app.yml/badge.svg)](https://github.com/shanmukh1315/calculator/actions)
![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![python](https://img.shields.io/badge/python-3.12+-blue)

A robust, modular **calculator** with a REPL interface, advanced design patterns (Strategy, Factory, Observer, Facade, Memento), pandas-backed history, configuration via `.env`, and **100% test coverage** enforced by GitHub Actions.

---

## Features

- **REPL** loop with prompts, `help`, and `exit`
- **Operations**: `add`, `sub`, `mul`, `div`, `pow`, `root`  
  (safe divide; power = `base exp`; root = `value degree`)
- **Design patterns**
  - **Strategy + Factory** for pluggable operations
  - **Observer** for event hooks (logging/autosave)
  - **Memento** (`Caretaker`) for **undo/redo**
  - **Facade**: single `Calculator` surface over subsystems
- **History with pandas**: in-memory `DataFrame` + CSV persistence
- **Config via `.env` / environment** with validation
- **User commands**: `history`, `clear`, `undo`, `redo`, `save`, `load`, `help`, `exit`
- **CI**: tests & coverage run on every push; build **fails** if coverage < 100%

---

## Project Structure
```
calculator/
├─ .github/workflows/
│ └─ python-app.yml # CI: pytest + coverage gate (100%)
├─ app/
│ ├─ init.py
│ ├─ calculation.py # Calculation dataclass + Calculator (Facade)
│ ├─ calculator_config.py # Config from env/.env (dotenv)
│ ├─ calculator_memento.py # Snapshot + Caretaker (Memento)
│ ├─ calculator_repl.py # REPL (CLI) + formatting
│ ├─ exceptions.py # Typed errors
│ ├─ history.py # pandas DataFrame history + CSV I/O (Observer hooks)
│ ├─ input_validators.py # parse_command / parse_numbers
│ └─ operations.py # Strategy + Factory: add/sub/mul/div/pow/root
├─ tests/
│ ├─ test_calculations.py
│ ├─ test_calculator_config.py
│ ├─ test_calculator_memento.py
│ ├─ test_calculator_repl.py
│ ├─ test_exceptions.py
│ ├─ test_history.py
│ ├─ test_input_validators.py
│ └─ test_operations.py
├─ .env.example # sample configuration
├─ .gitignore
└─ pyproject.toml # deps + pytest options (fail-under=100)
```


---

## Setup

Requires **Python 3.12+**.

```bash
# Clone and enter the project
git clone https://github.com/shanmukh1315/calculator.git
cd calculator

# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
python -m pip install --upgrade pip
pip install pytest pytest-cov pandas python-dotenv
```

**Run**
```
Interactive REPL:

python -m app.calculator_repl


Tip: in your shell, don’t type >>>—that’s the REPL prompt.
```
Commands
```
add|sub|mul|div|pow|root <numbers...>
history | clear | undo | redo | save | load | help | exit
```
**Examples**
```
>>> add 1 2 3
6.0
>>> pow 2 3
8.0
>>> root 27 3
3.0
```
**Tests & Coverage (100%)**
```
Run locally:

pytest
# or with a detailed coverage table:
pytest -q --cov=app --cov-branch --cov-report=term-missing


The repo enforces 100% coverage via pyproject.toml (fail-under=100) and the GitHub Actions workflow.
```
**Sample output**
```
============================================== tests coverage ==============================================
_____________________________ coverage: platform darwin, python 3.12.4-final-0 _____________________________

Name                        Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------------
app/__init__.py                 1      0      0      0   100%
app/calculation.py             13      0      0      0   100%
app/calculator_config.py       21      0      4      0   100%
app/calculator_memento.py      24      0      6      0   100%
app/calculator_repl.py         21      0      4      0   100%
app/exceptions.py               4      0      0      0   100%
app/history.py                 45      0      6      0   100%
app/input_validators.py        16      0      4      0   100%
app/operations.py              62      0     20      0   100%
-----------------------------------------------------------------------
TOTAL                         207      0     44      0   100%
Required test coverage of 100% reached. Total coverage: 100.00%
41 passed, 10 warnings in 1.00s
```
**Continuous Integration**

Workflow: .github/workflows/python-app.yml

Triggers: push and pull_request on main

Steps: setup Python → install deps → run pytest with coverage → enforce 100%

**Design Notes**
DRY & modular: arithmetic in operations.py; CLI in calculator_repl.py

Testability: REPL is injectable (I/O) and fully unit tested

Error handling: LBYL + EAFP; custom exceptions; defensive paths marked with # pragma: no cover

History & persistence: pandas DataFrame, CSV I/O, snapshot/restore via JSON split
