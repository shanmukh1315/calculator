from dataclasses import dataclass
import os
from dotenv import load_dotenv
from .exceptions import ConfigurationError

load_dotenv()

@dataclass(frozen=True)
class Config:
    autosave: bool
    history_path: str
    timestamp_format: str = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def from_env() -> "Config":
        autosave_str = os.getenv("CALC_AUTOSAVE", "true").strip().lower()
        if autosave_str not in {"true", "false"}:
            raise ConfigurationError("CALC_AUTOSAVE must be 'true' or 'false'")
        autosave = autosave_str == "true"

        history_path = os.getenv("CALC_HISTORY_PATH", "history.csv").strip()
        if not history_path:
            raise ConfigurationError("CALC_HISTORY_PATH must not be empty")

        ts_fmt = os.getenv("CALC_TIMESTAMP_FORMAT", "%Y-%m-%d %H:%M:%S").strip()
        return Config(autosave=autosave, history_path=history_path, timestamp_format=ts_fmt)
