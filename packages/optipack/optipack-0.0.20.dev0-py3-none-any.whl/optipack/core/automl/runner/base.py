from abc import ABC
try:
    from typing import Self
except:
    from typing_extensions import Self

# behave as factory: -> trainer or evaluator
class TorchRunner(ABC): 
    def __new__(cls: type[Self]): 
        ...
    
    def __init__(self, cfg ): 
        ...
    
    @abstractmethod
    def run(self, callbacks: list = []):
        self.on_runner_start()
        self.runner.run()

class TorchTrainer(ABC):

    def __new__(cls): 
        ...

    def __init__(self): 
        ...

    def on_runner_start(self): 
        # load model -> new or resume
        # logger start
        self.runner.on_epoch_start()

    def on_runner_end(self): 
        # logger end 
        # save model to registry
        ...

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def eval(self):
        pass

    @abstractmethod
    def run(self):
        pass

class TorchEvaluator(ABC): 
    ...

class SklearnRunner(ABC): 
    ...

class TFRunner(ABC):
    ...

