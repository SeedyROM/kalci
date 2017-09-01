"""A slightly convoluted and stupid way of logging important information.
"""
import sys
import traceback
import os

from functools import wraps

from . import settings


class logger:
    """A class that logs important info about the program.
    Same singleton implementation as the db module.
    """
    __instance = None
    def __new__(cls):
        """Abuse the __new__ function to allow this class persistances.
        Singleton hacks.
        """
        if logger.__instance is None:
            logger.__instance = object.__new__(cls)

            logger.__instance.log = open(
                os.path.join(settings.DATA_PATH, settings.LOG_NAME), 'a'
                )
            logger.__instance.terminal = sys.stdout

        return logger.__instance

    def write(self, message):
        """Conform our class to be passed as a writable file.
        """
        self.terminal.write(message + '\n')
        self.log.write(message + '\n')

    def flush():
        """Conform our class to be passed as a writable file.
        """
        pass

    @staticmethod
    def log(func):
        """Wraps a specified function and performs logging based on useful info.
        """
        @wraps(func)
        def wrapped(*args, **kwargs):
            """Log our information based on the settings.LOGGING level.
            """
            try:
                if settings.LOGGING > 1: logger().write(
                    f'Started executing function "{func.__name__}" in {__file__}...')

                func(*args, **kwargs)

                if settings.LOGGING > 1: logger().write(
                    f'Leaving function "{func.__name__}" in {__file__}...')
            except BaseException as e:
                # Catch all errors and raise them 'from None' to keep
                # later exceptions from bubbling up.
                raise e from None
                logger().write(f'Something went wrong...\n')
                traceback.print_tb(file=logger())

        return wrapped
