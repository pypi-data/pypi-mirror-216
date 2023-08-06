#!/usr/bin/env python3
from ..base import BaseClassfier
# Random forest classifier
from sklearn.ensemble import RandomForestClassifier


class Classifier(BaseClassfier):
    ModelType = RandomForestClassifier
