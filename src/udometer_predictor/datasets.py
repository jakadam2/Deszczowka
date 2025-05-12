from abc import ABC


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

    def get_iter(self):
        for i in range(len(self)):
            yield self[i] 
