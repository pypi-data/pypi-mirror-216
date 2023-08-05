from optipack.core.automl.builder.base import ModelBuilder
from optipack.sdk.optipack_logger import OptipackLogger

class TorchDefaultModelBuilder(ModelBuilder): 
    def __init__(self, mode: str, cfg: dict) -> None:

        logger = OptipackLogger(
            name = 'torch-model-builder-logger', 
            log_dir = './.otp_log/'
        )
        super().__init__(mode, cfg, logger)
    
    def build_model(self):
        try: 
            model_cls, kwargs = super().build_model()
            model = model_cls(**kwargs).to(self.cfg['device'])
            assert model, 'Invalid model instance'
            return model 
        except Exception as e: 
            self.logger.error(e)
            raise e

    def build_criterion(self):
        try: 
            criterion_cls , kwargs = super().build_criterion()
            criterion = criterion_cls(**kwargs).to(self.cfg['device'])
            assert criterion, 'Invalid criteriron instance'
            return criterion
        except Exception as e:
            self.logger.error(e)
            raise e
        
    def build_optimizer(self):
        try: 
            assert self.model, 'Expected model to build optimizer'
            optimizer_cls, kwargs = super().build_optimizer()
            optimizer = optimizer_cls(self.model.parameters(), **kwargs)
            assert optimizer, 'Invalid optimizer'
            return optimizer
        except Exception as e: 
            self.logger.error(e)
            raise e 
        
    def build(self):
        self.model = self.build_model()
        if self.mode == 'train': 
            self.logger.info(f'Building optimizer and criterion due to {self.mode} mode')
            self.optimizer = self.build_optimizer()
            self.criterion = self.build_criterion()

            return dict(
                model = self.model, 
                optimizer = self.optimizer, 
                criterion = self.criterion
            )
        
        return self.model


class TFDefaultModelBuilder(ModelBuilder): 
    ...

class SklearnDefaultModelBuilder(ModelBuilder): 
    ...
