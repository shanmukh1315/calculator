from __future__ import annotations
from .calculator_config import Config
from .calculation import Calculator
from .calculator_memento import Caretaker
from .history import History, LoggingObserver
from .input_validators import parse_command, parse_numbers
from .exceptions import CalculatorError

HELP_TEXT = """Commands:
  add|sub|mul|div|pow|root <numbers...>   Perform operation (pow: base exp, root: value degree)
  history                                 Show history
  clear                                   Clear history
  undo / redo                             Undo / redo last change
  save / load                             Save or load history CSV
  help                                    Show this help
  exit                                    Quit
"""

def make_calculator() -> Calculator:
    cfg = Config.from_env()
    hist = History(autosave=cfg.autosave, path=cfg.history_path, ts_format=cfg.timestamp_format)
    caretaker = Caretaker()
    calc = Calculator(history=hist, caretaker=caretaker, observers=[LoggingObserver()])
    return calc

def format_history(df) -> str:
    if df.empty:
        return "(no history)"
    rows = []
    for _, r in df.iterrows():
        rows.append(f"{r['ts']}  {r['op']}  {r['numbers']} = {r['result']}")
    return "\n".join(rows)

def repl(io_in=input, io_out=print) -> None:  # pragma: no cover
    io_out("Calculator REPL. Type 'help' for commands.")
    calc = make_calculator()
    while True:
        try:
            line = io_in(">>> ")
        except EOFError:
            break
        cmd, args = parse_command(line)
        if not cmd:
            continue
        try:
            if cmd in {"add", "sub", "mul", "div", "pow", "root"}:
                numbers = parse_numbers(args)
                c = calc.compute(cmd, numbers)
                io_out(c.result)
            elif cmd == "history":
                io_out(format_history(calc.history.df))
            elif cmd == "clear":
                calc.history.clear()
                io_out("history cleared")
            elif cmd == "undo":
                io_out("undone" if calc.undo() else "nothing to undo")
            elif cmd == "redo":
                io_out("redone" if calc.redo() else "nothing to redo")
            elif cmd == "save":
                calc.history.save()
                io_out("saved")
            elif cmd == "load":
                calc.history.load()
                io_out("loaded")
            elif cmd == "help":
                io_out(HELP_TEXT)
            elif cmd == "exit":
                io_out("bye!")
                break
            else:
                io_out("unknown command. type 'help'")
        except CalculatorError as e:
            io_out(f"error: {e}")
        except Exception as e:
            io_out(f"unexpected error: {e}")

if __name__ == "__main__":  # pragma: no cover
    repl()
