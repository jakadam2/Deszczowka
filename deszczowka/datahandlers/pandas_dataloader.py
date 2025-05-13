from torch.utils.data import Dataset
import pandas as pd
### tmp sol
import numpy as np
###


class PandasDataLoader(Dataset):
    def __init__(self, data: pd.DataFrame, targets: list[str], batch_size: int=None):
        self.data = data
        self.data["pred"] = np.random.rand(len(data))
        for step in range(1, 5):
            self.data[f"pred_+{step}"] = self.data["pred"].shift(-step)
        self.data = self.data.dropna()
        self.target = targets
        self.features = self.data.drop(columns=[*targets, "time", "rainfall[10m]"])
        self.labels = self.data[targets]

        if batch_size is None:
            self.batch_size = len(self.data)
        else:
            self.batch_size = batch_size

    def __iter__(self):
        for i in range(0, len(self.data), self.batch_size):
            yield self.features.iloc[i:i + self.batch_size], self.labels.iloc[i:i + self.batch_size]

    def __len__(self):
        return (len(self.data) + self.batch_size - 1) // self.batch_size

    def get_data(self):
        return self.features, self.labels
