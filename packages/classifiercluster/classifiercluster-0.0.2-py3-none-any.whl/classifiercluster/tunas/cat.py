import codefast as cf
import optuna
from ..base import BaseTuna
import catboost as cb

class Tuna(BaseTuna):
    MODEL_TYPE = 'catboost'

    def setup_model(self, trial: optuna.trial.Trial):
        param = {
            "iterations": trial.suggest_int("iterations", 100, 3000),
            "objective": trial.suggest_categorical("objective", ["Logloss", "CrossEntropy"]),
            "colsample_bylevel": trial.suggest_float("colsample_bylevel", 0.01, 0.1),
            "depth": trial.suggest_int("depth", 3, 12),
            "boosting_type": trial.suggest_categorical("boosting_type", ["Ordered", "Plain"]),
            "bootstrap_type": trial.suggest_categorical(
                "bootstrap_type", ["Bayesian", "Bernoulli", "MVS"]
            ),
            "used_ram_limit": "4gb",
            "verbose": 0
        }
        if param["bootstrap_type"] == "Bayesian":
            param["bagging_temperature"] = trial.suggest_float("bagging_temperature", 0, 10)
        elif param["bootstrap_type"] == "Bernoulli":
            param["subsample"] = trial.suggest_float("subsample", 0.1, 1)

        return cb.CatBoostClassifier(**param)

    def init_best_model(self, study: optuna.Study) -> 'Model':
        return cb.CatBoostClassifier(**study.best_params)
