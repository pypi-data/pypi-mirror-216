from abc import ABC, abstractmethod
from typing import Any


class ModelBuilder(ABC):
    def __init__(self, mode: str, cfg: dict, logger: Any) -> None:
        self.cfg = cfg
        self.logger = logger
        self.mode = mode

    def __get_module_kwargs(self, module_name: str):
        try:
            import importlib
            module_dict = self.cfg.get(module_name, {})
            assert module_dict, f'Invalid module with name {module_name}'
            module = importlib.import_module(module_dict['module'])
            return getattr(module, module_dict['cls_name']), module_dict['kwargs']
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_model(self):
        try:
            model_cls, kwargs = self.__get_module_kwargs('model')
            assert model_cls, f'Invalid model class'
            return model_cls, kwargs
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_optimizer(self):
        try:
            opt_cls, kwargs = self.__get_module_kwargs('optimizer')
            assert opt_cls, f'Invalid optimizer class'
            return opt_cls, kwargs
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_criterion(self):
        try:
            crit_cls, kwargs = self.__get_module_kwargs('criterion')
            assert crit_cls, f'Invalid criterion class'
            return crit_cls, kwargs
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build(self):
        pass


class DataBuilder(ABC):
    def __init__(self, mode: str, cfg: dict, logger: Any) -> None:
        self.mode = mode
        self.cfg = cfg
        self.logger = logger

    def __get_module_kwargs(self, module_name: str):
        try:
            import importlib
            module_dict = self.cfg.get(module_name, {})
            assert module_name, f'Invalid module with name {module_name}'
            module = importlib.import_module(module_dict['module'])
            return getattr(module, module_dict['cls_name']), module_dict['kwargs']
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_dataset(self):
        try:
            dataset_cls, kwargs = self.__get_module_kwargs('dataset')
            assert dataset_cls, f'Invalid dataset class'
            return dataset_cls, kwargs
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_dataloader(self):
        pass

    def build(self):
        pass


class MetricBuilder(ABC):
    def __init__(self, cfg: dict, logger: Any) -> None:
        self.cfg = cfg
        self.logger = logger

    def __get_module_kwargs(self, module_dict: dict):
        try:
            import importlib
            module = importlib.import_module(module_dict['module'])
            return getattr(module, module_dict['cls_name']), module_dict['kwargs']
        except Exception as e:
            self.logger.error(e)
            raise e

    @abstractmethod
    def build_metric(self, metric_name: str):
        metric_cls, kwargs = self.__get_module_kwargs(metric_name)
        return metric_cls, kwargs

    def build(self):
        pass
