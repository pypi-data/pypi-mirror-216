# user -> get optipack log or model's log
# adapter to use visualizer while logging

import logging
from optipack.core.logger import *
from optipack.core.visualizer import *
from typing import Any, MutableMapping, Mapping

class OptipackLogger(logging.LoggerAdapter):
    def __init__(self,
                 name: str,
                 logger: str = 'file',
                 visualizer: str = '',
                 log_dir: str = '.',
                 extra: Mapping[str, object] = {},
                 logger_kwargs: dict = {'level': logging.INFO},
                 visualizer_kwargs: dict = {'root_dir':'', 'run_folder': '', 'directory_list': []}
                 ) -> None:
        '''Logger adapter that connect logger and visualizer.

        Args:
            name (str): logger's name. .log file will have the same name.
            logger (str, optional): type of logger, including "console","file". Defaults to "file".
            visualizer (str, optional): type of visualizer, including "tensorboard", "aim", "". Defaults to "" when no visualizer is chosen.
            log_dir (str, optional): directory to the log storage. Defaults to ".".
            extra (Mapping[str, object], optional): metric and step mapping. Defaults to {}.
            visualizer_kwargs (str, optional): visualizer's args for directory creation. 
                Defaults to {"root_dir":"", "run_folder": "", "directory_list": {}}.

        Raises:
            RuntimeError: Initialization error
            AttributeError: Arguments passing error
        '''

        import os

        if not extra:
            extra = {
                'step': -1,
                'step_type': 'batch',
                'metric': {}
            }

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        self._epoch = 0
        try:
            LogCls = LOGGER_MAPPER.get(logger, None)
            assert LogCls, 'Invalid logger class'
            logger = LogCls(name=name, log_dir=log_dir, **logger_kwargs).logger
        except:
            raise RuntimeError('Unable to initialize logger')
        
        try:
            VisCls = VISUALIZER_MAPPER.get(visualizer, None)
            assert VisCls, 'No visualizer provided'
            if not visualizer_kwargs: 
                raise AttributeError('Visualizer required but no kwargs provided')
            visualizer_kwargs['name']=name
            if not visualizer_kwargs['root_dir']:
                visualizer_kwargs['root_dir'] = log_dir
            print(visualizer_kwargs)
            self.__vis_logger = VisCls(**visualizer_kwargs)
        except AssertionError as e:
            pass
        except AttributeError as e: 
            raise(e)

        super().__init__(logger, extra)

    def on_epoch_start(self, epoch: int):
        self._epoch = epoch
        self.logger.info(f'Start training at epoch {epoch}')

    def on_epoch_end(self, epoch: int):
        self._epoch = epoch
        self.logger.info(f'End training at epoch {epoch}')

    def process(self, msg: Any = None, kwargs: MutableMapping[str, Any] = None) -> tuple[Any, MutableMapping[str, Any]]:
        try:
            metric = kwargs.pop('metric', self.extra['metric'])
            step = kwargs.pop('step', self.extra['step'])
            step_type = kwargs.pop('step_type', self.extra['step_type'])
            assert step >= 0, 'Invalid step'
            assert step_type, 'Invalid step type'
            assert metric, 'Log normal message'

            if step_type == 'batch':
                self._epoch = step
                self.__vis_logger.log_metric(
                    title=f'{msg}-batch', step=self._epoch, metric_dict=metric)
            elif step_type == 'minibatch':
                # remember raising emtpy metric here
                self.__vis_logger.log_metric(
                    title=f'{msg}-minibatch', step=step, metric_dict=metric)
            else:
                raise TypeError('Invalid step type')
            to_str = f'[{step}/{self._epoch}]: {metric}'
            return to_str, kwargs
        except:
            return f'{msg}', kwargs
