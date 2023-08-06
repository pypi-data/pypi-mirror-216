import codefast as cf
import optuna
import xgboost as xgb

from ..base import BaseTuna


class Tuna(BaseTuna):
    MODEL_TYPE = 'xgb'

    def setup_model(self, trial: optuna.trial.Trial):
        xgb_params = {
            "tree_method": "gpu_hist",
            "max_depth": trial.suggest_int("max_depth", 2, 8),
            "learning_rate": trial.suggest_uniform("learning_rate", 0.05, 0.5),
            "n_estimators": trial.suggest_int("n_estimators", 1000, 5000),
            "gamma": trial.suggest_uniform("gamma", 0, 1),
            "subsample": trial.suggest_uniform("subsample", 0.1, 1),
            "colsample_bytree": trial.suggest_uniform("colsample_bytree", 0.1,
                                                      1),
            "reg_alpha": trial.suggest_uniform("reg_alpha", 0, 1),
            "reg_lambda": trial.suggest_uniform("reg_lambda", 0, 1)
        }
        return xgb.XGBClassifier(**xgb_params)

    def init_best_model(self, study: optuna.Study) -> 'Model':
        return xgb.XGBClassifier(**study.best_params)
