from .logger import Logger as Logger
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
    },
    "handlers":{
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "console":{
            "formatter": "std_out",
            "class": "handlers.TimedRotatingFileHandler",
            "level": "DEBUG"
        },
        "console":{
            "formatter": "std_out",
            "class": "handlers.TimedRotatingFileHandler",
            "level": "ERROR"
        }
    },
    "formatters":{
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    }
}