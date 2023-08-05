# - choose the wanted mllibrary
# - choose the wanted group of algorithm

from typing import Self

class AutoML(): 
    def __init__(self, 
        mode: str,
        library: str,
        config_dir:str, 
    ) -> None:
        ...
        # needs updating after AutoModel
        # from optipack.core.automl.runner import Trainer
        # from automl.evaluator import Evaluator
        # from automl.inferer import Inferer
        # from sdk.optipack_logger import OptipackLogger

        # self.logger = OptipackLogger(
        #     name = 'automl', 
        #     log_dir= './log'
        # )

        # mode_mapping = dict(
        #     train = Trainer,
        #     eval = Evaluator, 
        #     infer = Inferer
        # )

        # try: 
        #     RunnerCls = mode_mapping.get(mode, None)
        #     assert RunnerCls, 'Invalid Runner class' 
        #     self.auto_runner = RunnerCls(config_dir, library)
        # except Exception as e:
        #     self.logger.error(e)

    def build(): 
        ...

    def run(): 
        ...


        
        