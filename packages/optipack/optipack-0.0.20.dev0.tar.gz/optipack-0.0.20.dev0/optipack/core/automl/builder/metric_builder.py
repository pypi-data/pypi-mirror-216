from optipack.core.automl.builder.base import MetricBuilder
from optipack.sdk.optipack_logger import OptipackLogger


class TorchDefaultMetricBuilder(MetricBuilder):
    def __init__(self, cfg: dict) -> None:
        logger = OptipackLogger(name = 'torch-metric-builder-logger',
                                log_dir = './.otp_log/')
        super().__init__(cfg = cfg, logger=logger )

    def build_metric(self, metric_cfg: dict):
        try: 
            metric_cls, kwargs =  super().build_metric(metric_cfg)
            metric = metric_cls(**kwargs).to(self.cfg['device'])
            assert metric, f'Cannot initialize metric'
            return metric
        except Exception as e: 
            self.logger.error(e)
            raise e

    def build(self):
        cfg_metric_dict = self.cfg['watch_metric']
        metric_dict = dict()
        try:
            for m_k, metric in cfg_metric_dict.items():
                metric = self.build_metric(metric) 
                metric_dict[m_k] = metric
            return metric_dict
        except Exception as e: 
            self.logger.error(e)
            raise e
    

class SklearnDefaultMetricBuilder(MetricBuilder): 
    ...

class TFDefaultMetricBuilder(MetricBuilder): 
    ...
    