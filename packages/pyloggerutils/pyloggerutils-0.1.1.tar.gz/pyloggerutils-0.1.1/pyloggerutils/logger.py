from . import LOG_CONFIG
import logging
from logging.config import dictConfig
class Logger:

    name = "Logger"
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]
        pass
    
    def config_logger(self):
        dictConfig(LOG_CONFIG)
        self.logger = logging.getLogger(self.name)
    
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)