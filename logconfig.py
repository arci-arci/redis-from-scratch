from datetime import datetime
import logging
import os

LOG_FILE_NAME_FORMAT = "{:%Y-%m-%d}"
LOG_DIR_PATH = "./logs"
LOG_MESSAGE_FORMAT = "%(asctime)s %(levelname)s --- [%(name)s]    : %(message)s"


def create_logger() -> logging.Logger:
    if not os.path.isdir(LOG_DIR_PATH):
        os.mkdir(LOG_DIR_PATH)

    file_handler = logging.FileHandler(f"{LOG_DIR_PATH}/{LOG_FILE_NAME_FORMAT}.log".format(datetime.now()), encoding="utf-8")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_MESSAGE_FORMAT)
    
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger = logging.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger

