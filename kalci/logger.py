import sys
import traceback
import os

from functools import wraps

class logger:
    LOGGING = 1
    LOG_PATH = '/var/log/kalci'
    LOG_NAME = 'kalci.log'

    __instance = None
    def __new__(cls):
        if logger.__instance is None:
            logger.__instance = object.__new__(cls)

            try:
                os.makedirs(logger.LOG_PATH)
            except OSError:
                pass
            else:
                logger.__instance.log = open(os.path.join(logger.LOG_PATH, logger.LOG_NAME), 'w')


            logger.__instance.terminal = sys.stdout

        return logger.__instance

    def write(self, message):
        self.terminal.write(message + '\n')
        self.log(message + '\n')

    def flush():
        pass

    @staticmethod
    def log(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                logger().write(f'Started executing function "{func.__name__}" in {__file__}...')
                func(*args, **kwargs)
                logger().write(f'Leaving function "{func.__name__}" in {__file__}...')
            except BaseException as e:
                raise e from None
                logger().write(f'Something went wrong...\n')
                traceback.print_tb(file=logger())

        return wrapped
