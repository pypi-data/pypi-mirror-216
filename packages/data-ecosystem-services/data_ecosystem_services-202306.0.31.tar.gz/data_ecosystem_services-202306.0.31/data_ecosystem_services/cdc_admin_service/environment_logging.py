""" Module for python logging for cdc_tech_environment_service with minimal dependencies. """

import sys  # don't remove required for error handling
import os
import logging
import logging.config
import logging.handlers 
from logging.handlers import TimedRotatingFileHandler
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.sdk._logs import (
    LoggingHandler,
    LoggerProvider
)

from opentelemetry._logs import (

    set_logger_provider,
)

from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter


# Import from sibling directory ..\cdc_tech_environment_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "\\.."))
    ENV_SHARE_PATH = env_path + "\\share"
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "\\..\\share")))
    LOG_FILENAME = ENV_SHARE_PATH + "\\.pade_python_services_logging.txt"
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))
    env_path = os.path.dirname(os.path.abspath(sys.executable + "/.."))
    ENV_SHARE_PATH = env_path + "/share"
    sys.path.append(os.path.dirname(os.path.abspath(sys.executable + "/../share")))
    LOG_FILENAME = ENV_SHARE_PATH + "/pade_python_services_logging.txt"

FOLDER_EXISTS = os.path.exists(ENV_SHARE_PATH)
if not FOLDER_EXISTS:
    # Create a new directory because it does not exist
    os.makedirs(ENV_SHARE_PATH)


print(f"Log files stored at LOG_FILENAME:{LOG_FILENAME}")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
            
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "DEBUG", "handlers": ["logfile"]},
    "ocio_pade_dev": {"level": "DEBUG", "handlers": ["logfile"]},
}


class LoggerSingleton:
    """
    A Python wrapper class around OpenTelemetry Logger using a 
    singleton design pattern, so that the logger instance is created 
    only once and the same instance is used throughout the application.

    Raises:
        Exception: If an attempt is made to create another instance
                   of this singleton class.

    Returns:
        LoggerSingleton: An instance of the LoggerSingleton class.
    """
    _instance = None

    @staticmethod
    def instance():
        """Provides access to the singleton instance of the LoggerSingleton 
        class.

        This method ensures there is only one instance of the LoggerSingleton 
        class in the application.
        If an instance already exists, it returns that instance. If no 
        instance exists, it creates a new one and then returns that.
        """
        if LoggerSingleton._instance is None:
            LoggerSingleton()
        return LoggerSingleton._instance



    def __init__(self):
        """Initializes the singleton instance, if it doesn't exist yet.

        This method is responsible for ensuring that only a single instance 
        of the class is created. If an instance doesn't exist at the time of 
        invocation, it will be created. If an instance already exists, 
        the existing instance will be used.
        """
        if LoggerSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerSingleton._instance = self



        logger_provider = LoggerProvider()
        set_logger_provider(logger_provider)

        log_exporter = AzureMonitorLogExporter(connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"])
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

        # Attach LoggingHandler to root logger
        self.file_path = LOG_FILENAME
        os.makedirs(os.path.dirname(ENV_SHARE_PATH), exist_ok=True)
        # Create a console handler and set its log level to INFO
        format = LOGGING_CONFIG['formatters']['default']['format']
        datefmt = LOGGING_CONFIG['formatters']['default']['datefmt']

        self.azure_handler = LoggingHandler()

        formatter = logging.Formatter(format, datefmt)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(formatter)
        self.console_handler.setLevel(logging.getLevelName(LOGGING_CONFIG['handlers']['verbose_output']['level']))

        self.file_handler = TimedRotatingFileHandler(self.file_path, when="midnight", interval=1, backupCount=7)
        self.logger = logging.getLogger("data_ecosystem_services")
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.azure_handler)

        # Set the threshold of logger to INFO
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        """
        Get the logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger

    def force_flush(self):
        """This method forces an immediate write of all log 
        messages currently in the buffer.

        In normal operation, log messages may be buffered for
        efficiency. This method ensures that all buffered messages 
        are immediately written to their destination. It can be 
        useful in scenarios where you want to ensure that all 
        log messages have been written out, such as before ending 
        a program.
        """  
        for h in self.logger.handlers:
            h.flush()