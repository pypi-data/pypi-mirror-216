#!/usr/bin/env python3

from ..base import BaseClassfier
# Lightgbm model
from lightgbm import LGBMClassifier


class Classifier(BaseClassfier):
    ModelType = LGBMClassifier
