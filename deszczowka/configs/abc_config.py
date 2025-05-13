import json
from dataclasses import dataclass, fields
from typing import Any
import optuna


@dataclass
class ConfigHandler:
    var_type: str
    var_values: list[Any] | tuple[Any, Any]


@dataclass
class Config:
    def suggest(self, trial: optuna.Trial) -> dict:
        """
        Suggest hyperparameters from Optuna trial based on tuple-encoded ranges.
        """
        suggestions = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if val.var_type == "cat":
                suggestions[f.name] = trial.suggest_categorical(f.name, val.var_values)
            if val.var_type == "int":
                suggestions[f.name] = trial.suggest_int(f.name, val.var_values[0], val.var_values[1])
            if val.var_type == "float":
                suggestions[f.name] = trial.suggest_float(f.name, val.var_values[0], val.var_values[1])

        return suggestions

    def load_from_json(self, json_path: str):
        with open(json_path, "r") as f:
            config = json.load(f)
        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def save_to_json(self, json_path: str):
        with open(json_path, "w") as f:
            json.dump({f.name: getattr(self, f.name) for f in fields(self)}, f, indent=2)

