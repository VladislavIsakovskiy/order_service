import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

LOG_FOLDER = os.environ.get("LOGS_FOLDER_ROOT")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):  # noqa
        return logRecord.levelno <= self.__level


basedir = os.path.abspath(os.path.dirname(__file__))
log_folder = f"{basedir}/{LOG_FOLDER}"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig()
logger = logging.getLogger("")
logger.setLevel(LOGGING_LEVEL)

main_handler = RotatingFileHandler(f"{log_folder}/main.log", mode='a', maxBytes=50 * 1024 * 1024, backupCount=10,
                                   encoding="utf-8")
error_handler = RotatingFileHandler(f"{log_folder}/errors.log", mode='a', maxBytes=10 * 1024 * 1024, backupCount=5,
                                    encoding="utf-8")
main_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)

main_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
error_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
main_handler.setFormatter(main_format)
error_handler.setFormatter(error_format)

main_handler.addFilter(MyFilter(logging.WARNING))

logger.addHandler(main_handler)
logger.addHandler(error_handler)
