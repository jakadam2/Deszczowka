import optuna
from pathlib import Path
from abc import ABC, abstractmethod
from deszczowka.configs.abc_config import Config


class Model(ABC):
    def __init__(self, model_class):
        self.model_class = model_class

    def create_model(self, config: Config, trial: optuna.Trial):
        self.model = self.model_class(**config.suggest(trial))

    @abstractmethod
    def train(self, dataloader):
        pass

    @abstractmethod
    def predict(self, dataloader):
        pass

    @abstractmethod
    def save(self, path: Path):
        pass

    @abstractmethod
    def load(self, path: Path):
        pass
    