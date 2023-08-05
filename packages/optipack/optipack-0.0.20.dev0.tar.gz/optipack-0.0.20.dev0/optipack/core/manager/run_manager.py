from abc import ABC, abstractmethod
from fastcore.dispatch import *
from optipack.core.automl import *
from typing import Self

class RunManager(): 
    def __new__(cls: type[Self]
        ) -> Self:
        
        
    
        return super().__new__()

    def __init__(self) -> None:
        super().__init__()

    @typedispatch
    def run(self, trainer: trainer.Trainer): 
        ...

    @typedispatch
    def run(self, evaluator: evaluator.Evaluator): 
        ...

    @typedispatch
    def run(self, inferer: inferer.Inferer): 
        ...

