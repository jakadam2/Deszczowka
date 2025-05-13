import importlib
import yaml
from types import MethodType
import inspect
import logging
from udometer_predictor.datasets import Dataset

class FlexModel():
    def __init__(self, model_cls, logger, *model_args, **model_kwargs):
        self.model_cls = model_cls
        self.model_args = model_args
        self.model_kwargs = model_kwargs
        self.logger = logger
        pass

    def _train_one_epoch(self, model, dataset: Dataset):
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
            self.logger.info(f'Epoch {epoch + 1}/{epochs} successfully trained')
        return model
    
    def bind_train(self, func):
        self._train_one_epoch = MethodType(func, self)

    def to_yaml(self, path: str):
        config = {
            'model': f"{self.model_cls.__module__}.{self.model_cls.__name__}",
            'model_args': list(self.model_args),
            'model_kwargs': self.model_kwargs,
            'logger': getattr(self.logger, 'name', None)
        }
        src = inspect.getsource(self._train_one_epoch.__func__)
        config['train_one_epoch_code'] = src
        with open(path, 'w') as f:
            yaml.safe_dump(config, f)

    @classmethod
    def from_yaml(cls, path: str, logger=None):
        with open(path, 'r') as f:
            cfg = yaml.safe_load(f) or {}
        module_name, class_name = cfg['model'].rsplit('.', 1)
        module = importlib.import_module(module_name)
        model_cls = getattr(module, class_name)

        model_args = cfg.get('model_args', [])
        model_kwargs = cfg.get('model_kwargs', {})

        if logger is None:
            name = cfg.get('logger')
            logger = logging.getLogger(name) if name else logging.getLogger(__name__)

        instance = cls(model_cls, logger, *model_args, **model_kwargs)
        code = cfg.get('train_one_epoch_code')
        if code:
            local_ns = {}
            exec(code, globals(), local_ns)
            func = local_ns.get('_train_one_epoch') or next(iter(local_ns.values()))
            instance.bind_train(func)
        return instance