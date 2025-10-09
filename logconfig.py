from datetime import datetime
from logging import Logger, FileHandler, StreamHandler, Formatter, getLogger, INFO
import os
from commands import CommandEnum, CommandLenEnum

LOG_FILE_NAME_FORMAT = "{:%Y-%m-%d}"
LOG_DIR_PATH = "./logs"
LOG_MESSAGE_FORMAT = "%(asctime)s %(levelname)s %(thread)d --- [%(name)s]    : %(message)s"


def create_logger() -> Logger:
    if not os.path.isdir(LOG_DIR_PATH):
        os.mkdir(LOG_DIR_PATH)

    file_handler = FileHandler(f"{LOG_DIR_PATH}/{LOG_FILE_NAME_FORMAT}.log".format(datetime.now()), encoding="utf-8")
    stream_handler = StreamHandler()
    formatter = Formatter(LOG_MESSAGE_FORMAT)
    
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger = getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(INFO)

    return logger

def log_action(commad: CommandEnum, logger: Logger):
    def loggable(decoreted_fn):
        def wrapper(*args):
            
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