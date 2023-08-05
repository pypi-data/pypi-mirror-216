from optipack.core.logger.base import BaseLogger
import logging

class SplunkLogger(BaseLogger):
    def __init__(self,
                 name: str,
                 level: int = logging.DEBUG, 
                 config_path: str = 'core/logger/logger.cfg',
                 splunk_cfg: str = ''):
        super().__init__(name, config_path)

    def add_splunk_handler(self):
        # no token available
        raise NotImplementedError('Gimme token!!')


class FileLogger(BaseLogger):
    def __init__(self,
                 name: str,
                 mode: str = 'w',
                 level: int = logging.DEBUG,
                 log_dir: str = './log',
                 config_path: str = 'core/logger/logger.cfg'
                 ):
        super().__init__(name, config_path)
        self.log_dir = log_dir
        self.mode = mode
        self.add_file_handler()
        if level != logging.DEBUG: 
            self._logger.setLevel(level)

    def __set_log_path(self):
        import os
        try:
            if not os.path.exists(self.log_dir):
                os.mkdir(self.log_dir)
            return os.path.join(self.log_dir, f'{self.name}.log')
        except:
            raise NotADirectoryError(f'{self.log_dir} is unreachable.')

    def add_file_handler(self):
        import logging
        try:
            log_path = self.__set_log_path()
            file_handler = logging.FileHandler(log_path, mode=self.mode)
            file_handler.setFormatter(self._formatter)
            self._logger.addHandler(file_handler)
        except Exception as e:
            raise RuntimeError('Cannot create file handler')
        
    

if __name__ == '__main__':
    logger = BaseLogger(name='base-logger').logger
    logger.debug('hello there')
    logger.warning('hello you')

    file_logger = FileLogger(name='file-logger').logger
    file_logger.info('hello file logging')
