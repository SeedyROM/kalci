import sys
import traceback
import os

from functools import wraps

class logger:
    LOGGING = 2
    LOG_PATH = '.kalci'
    LOG_NAME = 'kalci.log'

    __instance = None
    def __new__(cls):
        if logger.__instance is None:
            logger.__instance = object.__new__(cls)

            try:
                if not os.path.exists(logger.LOG_PATH):
                    os.makedirs(logger.LOG_PATH)
            except OSError as e:
                print('Failed to setup logging...')
                exit(-1)
            else:
                print(os.path.join(logger.LOG_PATH, logger.LOG_NAME))
                logger.__instance.log = open(os.path.join(logger.LOG_PATH, logger.LOG_NAME), 'w+')


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
                if logger.LOGGING > 1: logger().write(
                    f'Started executing function "{func.__name__}" in {__file__}...')

                func(*args, **kwargs)

                if logger.LOGGING > 1: logger().write(
                    f'Leaving function "{func.__name__}" in {__file__}...')
            except BaseException as e:
                raise e from None
                logger().write(f'Something went wrong...\n')
                traceback.print_tb(file=logger())

        return wrapped
