from abc import ABC, abstractmethod
import logging

class BaseLogger(ABC): 
    def __init__(self, 
        name: str, 
        config_path: str = 'core/logger/logger.cfg', 
    ): 
        try: 
            import os
            from logging.config import fileConfig
            if 'OPTIPACK_PATH' in os.environ: 
                config_path = os.path.join(os.environ['OPTIPACK_PATH'], config_path)
            fileConfig(config_path)
            self.name = name
            self._logger = logging.getLogger(name=self.name)
            self._formatter = logging._handlers.data['consoleHandler']().__dict__['formatter']
        except Exception as e: 
            raise e
        
    @property
    def logger(self):
        return self._logger
