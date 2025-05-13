from .abc_model import Model
import joblib


class SklearnModel(Model):    
    def train(self, dataloader):
        x, y = dataloader.get_data()
        self.model.fit(x, y)

    def predict(self, dataloader):
        x, _ = dataloader.get_data()
        return self.model.predict(x)

    def save(self, path):
        joblib.dump(self.model, path)    

    def load(self, path):
        self.model = joblib.load(path)
