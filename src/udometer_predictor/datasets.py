from abc import ABC
import numpy as np

class Dataset(ABC):
    
    def __len__(self) -> int:
        raise NotImplementedError()

    def __getitem__(self, idx: int):
        raise NotImplementedError()
    
    @property
    def model_args(self):
        raise NotImplementedError()
    
    @property
    def model_kwargs(self):
        raise NotImplementedError()

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


class RandomLinearDataset(Dataset):

    def __init__(self, n_samples: int, n_features: int, noise_std: float = 0.1,
                 seed: int = None, n_batch: int = 1, test_size: float = 0.2):
        self.n_samples = n_samples
        self.n_features = n_features
        self.noise_std = noise_std
        self.seed = seed
        self.n_batch = max(1, n_batch)
        self.test_size = min(max(test_size, 0.0), 1.0)

        rng = np.random.default_rng(seed)
        X_all = rng.normal(size=(n_samples, n_features))
        w = rng.normal(size=(n_features,))
        b = rng.normal()
        noise = rng.normal(scale=noise_std, size=n_samples)
        y_all = X_all @ w + b + noise

        perm = rng.permutation(n_samples)
        n_test = int(n_samples * self.test_size)
        test_idx = perm[:n_test]
        train_idx = perm[n_test:]

        self.X_train = X_all[train_idx]
        self.y_train = y_all[train_idx]
        self.X_test = X_all[test_idx]
        self.y_test = y_all[test_idx]

        self._train_size = len(self.X_train)
        self._batch_size = int(np.ceil(self._train_size / self.n_batch))

    def __len__(self):
        return self.n_batch

    def __getitem__(self, idx: int):
        start = idx * self._batch_size
        end = min(start + self._batch_size, self._train_size)
        return self.X_train[start:end], self.y_train[start:end]

    @property
    def model_args(self):
        return []

    @property
    def model_kwargs(self):
        # return {'input_dim': self.n_features}
        return {}

    @property
    def test(self):
        return self.X_test, self.y_test

