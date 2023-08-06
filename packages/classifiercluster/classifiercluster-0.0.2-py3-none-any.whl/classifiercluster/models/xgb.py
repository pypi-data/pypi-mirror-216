#!/usr/bin/env python3

from xgboost import XGBClassifier

from ..base import BaseClassfier


class Classifier(BaseClassfier):
    ModelType = XGBClassifier

