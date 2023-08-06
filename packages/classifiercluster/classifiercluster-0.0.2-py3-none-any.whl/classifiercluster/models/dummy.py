#!/usr/bin/env python3

from ..base import BaseClassfier
from sklearn.dummy import DummyClassifier

class Classifier(BaseClassfier):
    ModelType = DummyClassifier
