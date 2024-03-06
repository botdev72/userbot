import logging
from os import execvp
from sys import executable
import os

class ConnectionHandler(logging.Handler):
    def emit(self, record):
        for X in ["OSError", "socket"]:
            if X in record.getMessage():
                os.system(f"kill -9 {os.getpid()} && python3 -m Amang")


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

formatter = logging.Formatter("[%(levelname)s] - %(name)s - %(message)s", "%d-%b %H:%M")
stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)

LOGS = logging.getLogger(__name__)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
