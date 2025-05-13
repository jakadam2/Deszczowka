import optuna
import pandas as pd
import wandb
from sklearn.metrics import root_mean_squared_error
from deszczowka.models.abc_model import Model
from pathlib import Path
from deszczowka.configs.abc_config import Config
from deszczowka.datahandlers.pandas_dataloader import PandasDataLoader


class Pipeline:
    def __init__(
        self,
        model: Model,
        data_path: Path,
        opt_config: Config,
        split_ratio: tuple[float, float, float] = (0.6, 0.2, 0.2),
        time_col: str = "time",
        project_name: str = "deszczowka",
        entity: str = "your_entity",
    ):
        self.model = model
        self.data_path = data_path
        self.opt_config = opt_config
        self.split_ratio = split_ratio
        self.time_col = time_col
        self.project_name = project_name
        self.entity = entity
        self.logger = wandb.init(
            project=self.project_name,
            config=self.opt_config,
            name=self.model.__class__.__name__,
        )
        self.data = pd.read_csv(data_path)
        self.data[self.time_col] = pd.to_datetime(self.data[self.time_col])
        self.train_dataloader, self.val_dataloader, self.test_dataloader = self.__split_data()

    def __split_data(self):
        train_size = int(len(self.data) * self.split_ratio[0])
        val_size = int(len(self.data) * self.split_ratio[1])

        train_data = self.data.iloc[:train_size]
        val_data = self.data.iloc[train_size:train_size + val_size]
        test_data = self.data.iloc[train_size + val_size:]

        train_dataloader = PandasDataLoader(train_data, targets=["rainfall[10m]"])
        val_dataloader = PandasDataLoader(val_data, targets=["rainfall[10m]"])
        test_dataloader = PandasDataLoader(test_data, targets=["rainfall[10m]"])

        return train_dataloader, val_dataloader, test_dataloader

    def __single_training(self, trial: optuna.Trial):
        self.model.create_model(self.opt_config, trial=trial)
        self.model.train(self.train_dataloader)
        pred = self.model.predict(self.val_dataloader)
        _y = self.val_dataloader.get_data()[1]
        return self.evaluate(pred, _y)
    
    def run(self, n_trials: int = 10):
        study = optuna.create_study(direction="minimize")
        study.optimize(self.__single_training, n_trials=n_trials)
        best_params = study.best_params
        self.logger.log(best_params)

        # for _x, _y in self.test_dataloader:
        #     self.model.test(_x, _y)

    def evaluate(self, pred, y):
        result = root_mean_squared_error(y, pred)
        self.logger.log({"rmse": result})
        return result
