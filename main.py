from deszczowka.models.sklearn_model import SklearnModel
from deszczowka.configs.lasso_config import LassoConfig
from deszczowka.pipeline import Pipeline
from sklearn.linear_model import Lasso
from pathlib import Path


if __name__ == "__main__":
    model = SklearnModel(Lasso)
    data_path = Path("/home/rusiek/Studia/viii_sem/Deszczowka/tmp.csv")
    opt_config = LassoConfig()
    pipeline = Pipeline(
        model=model,
        data_path=data_path,
        opt_config=opt_config
    )
    pipeline.run()