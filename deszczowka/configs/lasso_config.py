from deszczowka.configs.abc_config import Config, ConfigHandler
from dataclasses import dataclass, field


@dataclass
class LassoConfig(Config):
    """
    Configuration class for Lasso regression model.
    """
    alpha: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="float", var_values=(1e-3, 1e3), var_log=True)
    )
    fit_intercept: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="cat", var_values=[True, False])
    )
    precompute: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="cat", var_values=[True, False])
    )
    max_iter: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="int", var_values=(1000, 20000))
    )
    tol: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="float", var_values=(0.0001, 0.1), var_log=True)
    )
    warm_start: ConfigHandler = field(
        default_factory=lambda: ConfigHandler(var_type="cat", var_values=[True, False])
    )