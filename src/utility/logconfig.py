from datetime import datetime
import os
from logging import Logger, FileHandler, StreamHandler, Formatter, getLogger, INFO
from utility.commands import CommandEnum, CommandLenEnum

LOG_FILE_NAME_FORMAT = "{:%Y-%m-%d}"
LOG_DIR_PATH = "./logs"
LOG_MESSAGE_FORMAT = "%(asctime)s %(levelname)s %(thread)d --- [%(module)-12s] : %(message)-12s"

class LogSingleton:
    logger: Logger | None = None

    @classmethod
    def create_logger(cls) -> Logger:
        if not os.path.isdir(LOG_DIR_PATH):
            os.mkdir(LOG_DIR_PATH)

        if cls.logger != None:
            return cls.logger

        file_handler = FileHandler(f"{LOG_DIR_PATH}/{LOG_FILE_NAME_FORMAT}.log".format(datetime.now()), encoding="utf-8")
        stream_handler = StreamHandler()
        formatter = Formatter(LOG_MESSAGE_FORMAT)
        
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        cls.logger = getLogger(__name__)
        cls.logger.addHandler(file_handler)
        cls.logger.addHandler(stream_handler)
        cls.logger.setLevel(INFO)

        return cls.logger

def log_action(commad: CommandEnum):
    def loggable(decoreted_fn):
        def wrapper(*args):
            logger = LogSingleton.create_logger()

            match len(args):
                case CommandLenEnum.ONE:
                    logger.info(f"Running '{commad.name}' command")
                case CommandLenEnum.TWO:
                    logger.info(f"Running '{commad.name} %s' command", args[1])
                case CommandLenEnum.THREE:
                    logger.info(f"Running '{commad.name} %s %s' command", args[1], args[2])

            result = decoreted_fn(*args)
            return result
        return wrapper
    return loggable