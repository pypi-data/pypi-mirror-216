from typing import Any
from optipack.core.automl.builder.base import DataBuilder
from optipack.sdk.optipack_logger import OptipackLogger

class TorchDefaultDataBuilder(DataBuilder): 
    def __init__(self, mode: str, cfg: dict) -> None:
        logger = OptipackLogger(
            name = 'torch-data-builder-logger', 
            log_dir = './.otp_log/'
        )
        super().__init__(mode = mode, cfg = cfg, logger=logger)
        self.dataset_cls = None

    def split(self, dataset, val_ratio = 0.1, seed = 123): 
        try: 
            import torch
            from torch.utils.data import random_split
        except: 
            raise ImportError('Missing torch library')

        splitted = random_split(list(dataset), [val_ratio, 1-val_ratio], torch.Generator().manual_seed(seed))
        return splitted[0], splitted[1]

    def build_dataset(self, set_type: str ):
        try:
            if not self.dataset_cls: 
                self.dataset_cls, self.ds_kwargs = super().build_dataset()
                self.paths = self.ds_kwargs.get('paths', {})
                del self.ds_kwargs['paths']
            dataset = None
            if self.paths: 
                dataset = self.dataset_cls(self.paths[set_type], **self.ds_kwargs)
            else: 
                dataset = self.dataset_cls(**self.ds_kwargs)
            assert list(dataset), 'Invalid dataset instance'
            return dataset
        except Exception as e: 
            self.logger.error(e)
            raise e
    
    def build_dataloader(self, dataset: Any ):
        from torch.utils.data import DataLoader
        try: 
            dl_kwargs = self.cfg.get('data_loader')
            assert dl_kwargs, f'Invalid dataloader class'
            loader = DataLoader(dataset, **dl_kwargs)
            return loader
        except Exception as e: 
            self.logger.error(e)
            raise e   
    
    def build(self) -> dict:
        #TODO: rework this so it can be used for both torch and customized dataset
        if self.mode == 'train': 
            train_set = self.build_dataset(set_type='train')
            train_loader = self.build_dataloader(train_set)
            if self.paths.get('val', ''): 
                val_set = self.build_dataset(set_type='val')
                val_loader = self.build_dataloader(val_set)
                return dict(
                    train_loader = train_loader,
                    val_loader = val_loader
                )
            test_set = self.build_dataset(set_type='test')
            val_set = self.split_dataset(test_set)
            del test_set
            val_loader = self.build_dataloader(val_set)
            return dict(
                train_loader = train_loader,
                val_loader = val_loader
            )
        
        test_set = self.build_dataset(set_type='test')
        test_loader = self.build_dataloader()
        return dict(test_loader = test_loader)
    
class TFDefaultDataBuilder(DataBuilder):
    ...

class SklearnDefaultDataBuilder(DataBuilder):
    ...


