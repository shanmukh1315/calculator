import os
import importlib
import app.calculator_config as cc
import pytest
from app.exceptions import ConfigurationError

def test_config_defaults(monkeypatch):
    monkeypatch.delenv("CALC_AUTOSAVE", raising=False)
    monkeypatch.delenv("CALC_HISTORY_PATH", raising=False)
    importlib.reload(cc)
    cfg = cc.Config.from_env()
    assert isinstance(cfg.autosave, bool) and cfg.history_path

def test_config_validation(monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "maybe")
    with pytest.raises(ConfigurationError):
        cc.Config.from_env()

def test_config_empty_history_path(monkeypatch):
    monkeypatch.setenv("CALC_AUTOSAVE", "true")
    monkeypatch.setenv("CALC_HISTORY_PATH", "")
    importlib.reload(cc)
    with pytest.raises(ConfigurationError):
        cc.Config.from_env()
