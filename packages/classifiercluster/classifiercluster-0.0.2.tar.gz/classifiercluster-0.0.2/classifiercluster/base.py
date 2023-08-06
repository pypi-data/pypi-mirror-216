#!/usr/bin/env python3
from abc import ABC, abstractmethod

import codefast as cf
import optuna
import pandas as pd
from sklearn.model_selection import KFold, cross_validate


class BaseClassfier(object):
    """Base Class for all classifiers.

    Keyword Args:
        timeout (int, optional): Seconds before request is killed.
        verify (bool, str, optional): SSL Certificate verification for
            :ref:`Requests Verification <requests:verification>`.

    Example:
        >>> 
    """

    def __init__(self, **kwargs):
        for key, item in list(kwargs.items()):
            setattr(self, key, item)

        # safe check
        self.timeout = getattr(self, "timeout", 2)
        self.verify = getattr(self, "verify", True)
        self.model = self.reset_model()

    def reset_model(self, **kwargs):
        return self.ModelType(**kwargs)

    def _get(self, url, params=None, headers=None):
        pass

    def _post(self, url, data=None, json=None, params=None, headers=None):
        pass

    def fit(self, X, y, **kwargs):
        """fit the model

        Args:
            X (pd.dataframe): X data
            y (pd.Series): y data
        """
        self.model.fit(X, y, **kwargs)

    def predict(self, X):
        """predict the model

        Args:
            X (pd.dataframe): X data
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """predict the model

        Args:
            X (pd.dataframe): X data
        """
        return self.model.predict_proba(X)

    def set_params(self, **kwargs):
        self.model.set_params(**kwargs)
        return self


class BaseTuna(ABC):
    MODEL_TYPE: str = 'base_model'

    def __init__(self):
        pass

    def objective(self, X, y, trial, cv, scoring):
        model = self.setup_model(trial)
        scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=3)
        return scores['test_score'].mean()

    @abstractmethod
    def setup_model(self, study: optuna.Study) -> 'Model':
        """ Set model to be used in objective function
        Example:
            params = {}
            model = xgb.XGBClassifier(**params)
        """

    def find_best_study(self,
                        X,
                        y,
                        n_trials=100,
                        scoring: str = 'roc_auc',
                        direction: str = "maximize") -> optuna.Study:
        """ Find best params for model
        """
        cv = KFold(n_splits=5, shuffle=True, random_state=42)
        study = optuna.create_study(direction=direction,
                                    pruner=optuna.pruners.MedianPruner(
                                        n_startup_trials=5,
                                        n_warmup_steps=10,
                                        interval_steps=10))
        study.optimize(lambda trial: self.objective(X, y, trial, cv, scoring),
                       n_trials=n_trials,
                       gc_after_trial=True,
                       show_progress_bar=True)
        cf.info([self.MODEL_TYPE,
                 'best params', study.best_params])
        cf.info([self.MODEL_TYPE,
                 'best value', study.best_value])
        return study

    @abstractmethod
    def init_best_model(self, study: optuna.Study) -> 'Model':
        """ Initialize model with best params found by optuna
        """

    def fit(self, model, X, y) -> 'Model':
        """ Fit model with best params found by optuna
        """
        model.fit(X, y)
        return model

    def make_prediction(self,
                        model,
                        test,
                        sub,
                        target_column: str,
                        export_to: str,
                        proba: bool = True) -> pd.DataFrame:
        if proba:
            sub[target_column] = model.predict_proba(test)[:, 1]
        else:
            sub[target_column] = model.predict(test)
        sub.to_csv(export_to, index=False)
        cf.info([self.MODEL_TYPE, 'prediction exported to', export_to])
        return sub

    def pipeline(self,
                 X,
                 y,
                 test,
                 sub,
                 target_column: str,
                 export_to: str,
                 n_trials: int = 100,
                 scoring: str = 'roc_auc',
                 direction: str = "maximize"):
        """ Pipeline for finding best params and making prediction
        Args:
            X (pd.dataframe): X data
            y (pd.Series): y data
            test (pd.dataframe): test data
            sub (pd.dataframe): submission data
            target_column (str): target column name
            export_to (str): path to export prediction
            n_trials (int, optional): number of trials to run. Defaults to 100.
            scoring (str, optional): scoring method. Defaults to 'roc_auc'.
            direction (str, optional): direction of optimization. Defaults to "maximize".
        """
        study = self.find_best_study(X, y, n_trials, scoring, direction)
        model = self.init_best_model(study)
        model = self.fit(model, X, y)
        self.make_prediction(model, test, sub, target_column, export_to)
