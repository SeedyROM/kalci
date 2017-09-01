import sys
import traceback
import os

from functools import wraps

from . import settings


class logger:
    __instance = None
    def __new__(cls):
        if logger.__instance is None:
            logger.__instance = object.__new__(cls)

            logger.__instance.log = open(os.path.join(settings.DATA_PATH, settings.LOG_NAME), 'a')
            logger.__instance.terminal = sys.stdout

        return logger.__instance

    def write(self, message):
        self.terminal.write(message + '\n')
        self.log.write(message + '\n')

    def flush():
        pass

    @staticmethod
    def log(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                if settings.LOGGING > 1: logger().write(
                    f'Started executing function "{func.__name__}" in {__file__}...')

                func(*args, **kwargs)

                if settings.LOGGING > 1: logger().write(
                    f'Leaving function "{func.__name__}" in {__file__}...')
            except BaseException as e:
                raise e from None
                logger().write(f'Something went wrong...\n')
                traceback.print_tb(file=logger())

        return wrapped
