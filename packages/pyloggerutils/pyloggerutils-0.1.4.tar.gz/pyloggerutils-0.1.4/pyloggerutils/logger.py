from . import LOG_CONFIG, LOG_DATE_FORMAT, LOG_FORMAT_LIMITERS
import os
from datetime import datetime
# from logging.handlers import File
from logging import getLogger
from logging.config import dictConfig
import inspect
class Logger:

    name = "Logger"
    add_index = 3
    def __init__(self, **kwargs):
        if "name" in kwargs:
            self.name = kwargs["name"]
        self.config_logger()
    
    def config_logger(self):
        dictConfig(LOG_CONFIG)
        self.logger = getLogger(self.name)

    def __get_file_name__(self, file_name):
        return os.path.basename(file_name)

    def __get_bot_name__(self, file_name):
        return os.path.splitext(self.__get_file_name__(file_name))[0]

    def __get_frameinfo(self, add_index=False):
        innerframe = inspect.currentframe()
        outerframes = inspect.getouterframes(innerframe)
        if not add_index:
            add_index = self.add_index
        for index, frame in enumerate(outerframes):
            if(frame.function == "__get_frameinfo"):
                # add_index - Which function calls this function
                # +1 -> either debug, info, warning, error functions which is calling this function
                # +2 -> The Function that calls the above log functions, n -> until the top most function
                index += add_index
                break
        return outerframes[index]

    def msg(self, msg):
        frame_info = self.__get_frameinfo()
        function_name = frame_info.function
        module_name = self.__get_bot_name__(frame_info.filename)
        log_level = self.__get_frameinfo(add_index=2)
        log_level = log_level.function.split(".")
        log_level = f"[{log_level[len(log_level)-1].rjust(8).upper()}]"
        # msgdate= f"{datetime.strftime(datetime.now(), LOG_DATE_FORMAT)}"
        class_fun = f"[{module_name.rjust(10)}.{function_name.ljust(10)}]"

        msg = f"- {class_fun} - {log_level} : {msg}"
        return msg

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(self.msg(msg), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(self.msg(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(self.msg(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(self.msg(msg), *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(self.msg(msg), *args, **kwargs)