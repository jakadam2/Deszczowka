import importlib
import yaml
from abc import ABC
from udometer_predictor.datasets import Dataset

class FlexModel(ABC):
    def __init__(self, model_cls, logger, *model_args, **model_kwargs):
        self.model_cls = model_cls
        self.model_args = model_args
        self.model_kwargs = model_kwargs
        self.logger = logger
        pass

    def _train_one_epoch(self, model, dataset: Dataset) -> float:
        raise NotImplementedError()
    
    def _create_model(self, dataset: Dataset):
        args = [*dataset.model_args, *self.model_args]
        kwargs = {**dataset.model_kwargs, **self.model_kwargs}
        model = self.model_cls(*args, **kwargs)
        return model

    def train(self, dataset: Dataset, epochs: int = 1, train_params = None):
        model = self._create_model(dataset)
        for epoch in range(epochs):
            self._train_one_epoch(model, dataset)
        return model

    @classmethod
    def from_yaml(cls, path: str, logger=None):
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f)

        module_name, class_name = cfg['model'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        model_cls = getattr(module, class_name)

        model_args = cfg.get('model_args', [])
        model_kwargs = cfg.get('model_kwargs', {})

        return cls(model_cls, logger, *model_args, **model_kwargs)