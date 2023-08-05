import numpy as np
import matplotlib
from abc import ABC
try: 
    import torch
except: 
    raise ImportError('Missing torch library')

class OtpDataType(ABC):
    def __init__(self, item) -> None:
        self._item = item

    def __str__(self) -> str:
        return self.__name__

    @property
    def item(self):
        return self._item


class OtpImage(OtpDataType):
    def __init__(self, item, max_dim: int = 3, min_dim: int = 2, format: str = '') -> None:

        if isinstance(item, torch.Tensor):
            assert item.dim() <= max_dim and item.dim(
            ) >= min_dim, 'Expected torch.Tensor should have dim = 2 or dim = 3'
            self.format = 'CHW'
            self.dim = item.dim()

        elif isinstance(item, np.ndarray):
            assert item.ndim <= max_dim and item.ndim >= min_dim, 'Expected numpy.ndarray should have dim = 2 or dim = 3'
            self.format = 'HWC'
            self.dim = item.ndim
        else:
            raise AssertionError(
                'Expecting torch.Tensor or numpy.ndarray for casting')

        if self.dim == min_dim:
            self.format = 'HW'
        elif format:
            self.format = format
        super(OtpImage, self).__init__(item)


class OtpImageBatch(OtpImage):
    def __init__(self, item, mode: str = 'training') -> None:
        if mode == 'training' and isinstance(item, torch.Tensor):
            fm = item[0]
            fm = torch.unsqueeze(fm, 1)

        else:
            fm = item
        super().__init__(fm, max_dim=4, format='NCHW')


class OtpFigure(OtpDataType):
    def __init__(self, item) -> None:
        assert isinstance(item, matplotlib.pyplot.figure), \
            f'Expected {type(matplotlib.pyplot.figure)}, got {type(item)}'
        super().__init__(item)


class OtpHistogram(OtpDataType):
    def __init__(self, item) -> None:
        assert isinstance(item, torch.Tensor), \
            f'Expected {type(torch.Tensor)}, got {type(item)}'
        super().__init__(item)


class OtpVideo(OtpDataType):
    def __init__(self, item) -> None:
        assert isinstance(item, torch.Tensor), \
            f'Expected {type(torch.Tensor)}, got {type(item)}'
        super().__init__(item)


class OtpEmbedding(OtpDataType):
    def __init__(self, mat) -> None:
        raise NotImplementedError
