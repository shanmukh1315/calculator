from app.calculator_repl import repl
from io import StringIO

def run_repl_script(lines):
    output = []
    it = iter(lines)
    def fake_in(_prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError
    def fake_out(msg):
        output.append(str(msg))
    repl(io_in=fake_in, io_out=fake_out)
    return "\n".join(output)

def test_repl_happy_path(tmp_path, monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "false")
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "h.csv"))
    out = run_repl_script([
        "add 1 2",
        "pow 2 3",
        "root 27 3",
        "history",
        "undo",
        "redo",
        "save",
        "load",
        "clear",
        "help",
        "exit",
    ])
    assert "3.0" in out and "8.0" in out and "bye!" in out

def test_repl_errors(tmp_path, monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "false")
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "h2.csv"))
    out = run_repl_script([
        "div 1 0",
        "root 9 0",
        "pow 2",
        "noop",
        "exit",
    ])
    assert "error:" in out

def test_repl_undo_redo_when_empty_and_help(tmp_path, monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "false")
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "h3.csv"))

    out = run_repl_script([
        "undo",
        "redo",
        "help",
        "unknown",
        "exit",
    ])
    assert "nothing to undo" in out
    assert "nothing to redo" in out
    assert "Commands:" in out
    assert "unknown command" in out

def test_repl_immediate_eof(tmp_path, monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "false")
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "h4.csv"))
    out = run_repl_script([])
    assert "Calculator REPL" in out

def test_repl_history_when_empty(tmp_path, monkeypatch):
    # hits format_history(df) empty branch and that command’s print path
    monkeypatch.setenv("CALC_AUTOSAVE", "false")
    monkeypatch.setenv("CALC_HISTORY_PATH", str(tmp_path / "fresh.csv"))
    out = run_repl_script([
        "history",   # no calculations yet → "(no history)"
        "exit",
    ])
    assert "(no history)" in out
    assert "bye!" in out
