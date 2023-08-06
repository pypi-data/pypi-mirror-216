#!/usr/bin/env python3

from ..base import BaseClassfier
# Catboost classifier
import catboost as cb


class Classifier(BaseClassfier):
    ModelType = cb.CatBoostClassifier

    def reset_model(self, **kwargs):
        kwargs.setdefault('verbose', False)
        return self.ModelType(**kwargs)