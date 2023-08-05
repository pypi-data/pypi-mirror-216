"""
The wrapper for visualizers so that you can visualize metrics and scalars within simple logger command

Raises:
    RuntimeError: _description_
    NotImplementedError: _description_
"""

from optipack.core.visualizer.base import BaseVisualizer
from fastcore.dispatch import *
from optipack import typing
from threading import current_thread


class TensorboardVisualizer(BaseVisualizer):
    """Tensorboard that maps with normal logger
        Supported visualization: 
            - scalar
            - image
            - batch_images
            - figure
            - histogram
    """

    def __init__(self,
                 name: str,
                 root_dir: str,
                 run_folder: str= '',
                 **kwargs
                 ) -> None:
        
        try: 
            from torch.utils.tensorboard import SummaryWriter
        except: 
            raise ImportError('Missing Torch library')
        # the folder will be changed when optipack tracker is coded
        super().__init__(name, root_dir, run_folder)
        log_path = self.__create_log_dir(**kwargs)
        self.__writer = SummaryWriter(log_path)
        self.verbose = True

    def __create_log_dir(self, **kwargs):
        import os
        dirs = ['tensorboard']
        if 'directory_list' in kwargs:
            dirs += kwargs['directory_list']
        else:
            dirs.append(self.run_folder)
        log_path = self.root_dir
        try:
            for d in dirs:
                if not os.path.exists(log_path):
                    os.mkdir(log_path)
                log_path = os.path.join(log_path, d)
            print(f'Created tb log_path {log_path}')
            return log_path
        except:
            raise NotADirectoryError(f'{log_path} is unreachable.')

    def log_metric(
        self,
        title: str,
        step: int,
        metric_dict: dict
    ):
        from concurrent.futures import ThreadPoolExecutor, wait
        try:
            keys = [f'{title}/{k}' for k in list(metric_dict.keys())]
            metrics = dict(zip(keys, list(metric_dict.values())))
            self._step = step
        except Exception as e:
            raise RuntimeError(
                f'Error {e} happened while processing keys and metrics')

        try:
            executor = ThreadPoolExecutor()
            futures = wait([executor.submit(self._log_tb, k,v)
                  for k,v in metrics.items()
                  ])
            print(futures)
            self.__writer.flush()
            executor.shutdown()
        except Exception as e:
            raise RuntimeError(
                f'Error {e} happened while attempting threading execution')

    @typedispatch
    def _log_tb(self, tag: str, scalar: float):
        self.__writer.add_scalar(tag, scalar, self._step)

    @typedispatch
    def _log_tb(self, tag: str, image: typing.OtpImage):
        # item = image.get_item()
        try:
            self.__writer.add_image(
                tag, image.item, self._step, dataformats=image.format)
            self.__writer.flush()
        except:
            raise RuntimeError('Cannot write image to Tensorboard')

    @typedispatch
    def _log_tb(self, tag: str, image_batch: typing.OtpImageBatch):
        self.__writer.add_images(
            tag, image_batch.item, self._step, dataformats=image_batch.format)
        self.__writer.flush()

    @typedispatch
    def _log_tb(self, tag: str, figure: typing.OtpFigure):
        self.__writer.add_figure(tag, figure.item, self._step)


class AimVisualizer(BaseVisualizer):
    def __init__(self,
                 name: str,
                 root_dir: str,
                 run_folder: str) -> None:
        raise NotImplementedError('Waiting to be implemented :)')


if __name__ == '__main__':
    import PIL
    import numpy as np
    img = PIL.Image.open('optipack/asset/logo-large.png')
    np_arr = np.asarray(img)

    tb_vis = TensorboardVisualizer(
        name='tb-logger', root_dir='./log', run_folder='test-tb')

    from timeit import timeit
    time = timeit(str(
        tb_vis.log_metric(
            title=f'batch', step=1, metric_dict={
                'loss': 0.01,
                'accuracy': 0.99,
                'lr': 0.9123,
                'lr1': 1,
                'lr2': 2,
                'image0': typing.OtpImage(np_arr),
                'image': typing.OtpImage(np_arr),
                'images': typing.OtpImageBatch(np.asarray([np_arr, np_arr]))
            })), number=10000
    )
    print(time)
