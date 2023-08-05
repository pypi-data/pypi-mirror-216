from abc import ABC, abstractmethod
from typing import List, Dict
from optipack.sdk.optipack_logger import OptipackLogger
from optipack.core.automl import builder
try:
    from typing import Self
except:
    from typing_extensions import Self

logger = OptipackLogger(name='default-logger', log_dir='./.opt_log/')


class AutoModel(ABC):
    def __new__(cls: type[Self],
                lib_name: str = '',
                mode: str = '',
                cfg_dir: str = '',
                log_dir: str = './log',
                **kwargs
                ) -> Self:

        try:
            assert mode in ['train', 'eval'], f'Invalid mode {mode}'
            if cls is AutoModel:
                AutoModelCls = LIB_MAPPER.get(lib_name, None)
                assert AutoModelCls, 'We may not implemented this library :)'
                logger.info(
                    f'Initializing auto modelling for lib {lib_name} ...')
                return super(AutoModel, cls).__new__(AutoModelCls)

            return super(AutoModel, cls).__new__(cls, mode, cfg_dir, log_dir, **kwargs)

        except Exception as e:
            logger.error(e)
            raise e

    def __init__(self,
                 mode: str = 'train',
                 cfg_dir: str = '',
                 log_dir: str = './log',
                 ):
        from ..fileio.reader_misc import read_yaml

        self.mode = mode
        self.cfg = read_yaml(cfg_dir)
        self.logger = OptipackLogger(name='auto-model-logger', log_dir=log_dir)

    @abstractmethod
    def build(self,
              model_builder_cls: builder.ModelBuilder,
              data_builder_cls: builder.DataBuilder,
              metric_builder_cls: builder.MetricBuilder
              ):
        self.model_builder = model_builder_cls(mode = self.mode, cfg = self.cfg)
        self.data_builder = data_builder_cls(mode = self.mode, cfg= self.cfg)
        self.metric_builder = metric_builder_cls(self.cfg)

    @abstractmethod
    def run(self):
        pass

    def load_builder_from_cfg(self):
        pass


class AutoModelTorch(AutoModel):
    def __init__(self,
                 mode: str,
                 cfg_dir: str,
                 log_dir: str = './log',
                 **kwargs
                 ):
        super().__init__(mode=mode, cfg_dir=cfg_dir, log_dir=log_dir)
        from ..automl.runner import TorchTrainer, TorchEvaluator
        self.RUNNER_MAPPER = dict(
            train = TorchTrainer, 
            val = TorchEvaluator
        )

    def build(self,
              model_builder_cls=builder.TorchDefaultModelBuilder,
              data_builder_cls=builder.TorchDefaultDataBuilder,
              metric_builder_cls=builder.TorchDefaultMetricBuilder
              ):
        from ..automl.runner import TorchRunnerConfig
        super().build(model_builder_cls, data_builder_cls, metric_builder_cls)

        model_dict = self.model_builder.build()
        data_dict = self.data_builder.build()
        metric_dict = self.metric_builder.build()
        print(model_dict)
        print(data_dict)
        print(metric_dict)
        self.runner_cfg = TorchRunnerConfig(
            self.mode, model_dict, data_dict, metric_dict)

        del self.model_builder
        del self.data_builder
        del self.metric_builder

    def run(self):
        runner_cls = self.RUNNER_MAPPER.get(self.mode)
        self.runner = runner_cls(self.runner_cfg)
        early_stop_callback = EarlyStopCallback()
        self.runner.on_start()
        self.runner.run(callbacks = [early_stop_callback])
        self.runner.on_end()


LIB_MAPPER = dict(
    pytorch=AutoModelTorch
)


if __name__ == '__main__':
    auto_model = AutoModel('pytorch', 'train', log_dir='test-log-fac')
