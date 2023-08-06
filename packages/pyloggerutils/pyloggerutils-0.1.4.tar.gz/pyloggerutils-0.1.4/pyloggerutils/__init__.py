LOG_DATE_FORMAT = "%d-%m-%Y %I:%M:%S"
LOG_FORMAT_LIMITERS = {
    "MODULE": 40
}
LOG_LEVELS = {
    "DEBUG": 1,
    "INFO": 2,
    "WARNING": 3,
    "CRITICAL": 4,
    "ERROR": 5
}

LOG_CONFIG = {
    "version": 1,
    "root": {
        "handlers": ["console", "fileHandler", "fileErrorHandler"],
        "level": "NOTSET"
    },
    "handlers":{
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "fileHandler":{
            "formatter": "std_out",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": "debug.log"
            # "args": ('testing.log','w0',0,5)
        },
        "fileErrorHandler":{
            "formatter": "std_out",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "ERROR",
            "filename": "error.log"
        }
    },
    "formatters":{
        "std_out": {
            # "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s",
            "format": "%(asctime)s - %(name)s [%(processName)s] %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    }
}
from .logger import Logger as Logger