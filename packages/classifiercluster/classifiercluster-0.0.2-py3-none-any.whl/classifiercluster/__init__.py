import importlib
import logging
import pkgutil

logger = logging.getLogger(__name__)
__version__ = "0.0.1"
__author__ = "Gaoang Lau"
__email__ = "Gaoanglau@gmail.com"
__license__ = "GPLv3"


class Classifiers(object):
    """Base Factory class to create classifier instances

    >>> clf = Classifiers(**kwargs)
    >>> instance = clf.name
    >>> instance.fit(X, y)

    Example:
    >>> c = Classifiers()
    >>> c.xgb.fit(X, y)
    >>> y_preds = c.xgb.predict(X)

    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        # validate some required fields
        self.kwargs["debug"] = bool(kwargs.pop("debug", False))
        self.kwargs["timeout"] = int(kwargs.pop("timeout", 2))
        module = importlib.import_module("classifiercluster.models")
        self.available_models = [
            i.name for i in pkgutil.iter_modules(module.__path__)
        ]
        self.instances = {}
        # print(module)
        # print(module.__path__)
        # print(self.available_models)

    def __getattr__(self, attr):
        """Get instance of classifier class"""
        if attr not in self.available_models:
            return self.__getattribute__(attr)

        if attr not in self.instances:
            self.instances[attr] = self._create_instance(attr)
        return self.instances[attr]

    def _create_instance(self, attr: str):
        """Create instance of classifier class"""
        classifier_module = importlib.import_module("{}.{}".format(
            "classifiercluster.models", attr))
        instance = getattr(classifier_module, "Classifier")(**self.kwargs)
        logger.info("Created instance of {}".format(attr))
        return instance


class Tunas(object):
    """Base Factory class to create tuna instances
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        module = importlib.import_module("classifiercluster.tunas")
        self.available_models = [
            i.name for i in pkgutil.iter_modules(module.__path__)
        ]
        self.instances = {}

    def __getattr__(self, attr):
        """Get instance of tuna class"""
        if attr not in self.available_models:
            print("Available models: {}".format(self.available_models))
            return self.__getattribute__(attr)

        if attr not in self.instances:
            self.instances[attr] = self._create_instance(attr)
        return self.instances[attr]

    def _create_instance(self, attr: str):
        """Create instance of classifier class"""
        classifier_module = importlib.import_module("{}.{}".format(
            "classifiercluster.tunas", attr))
        instance = getattr(classifier_module, "Tuna")(**self.kwargs)
        logger.info("Created instance of {}".format(attr))
        return instance


classifiers = Classifiers()
tunas = Tunas()

