"""A simple database connection API with some helpful decorators.
"""
import atexit
import sqlite3
import os

from functools import wraps

from .logger import logger
from . import settings


class db:
    """ Singleton pattern type database connection helper.
    """
    __instance = None
    def __new__(cls, path_to_db=settings.DATA_PATH):
        """Abuse the __new__ function to allow this class persistances.
        Singleton hacks.
        """
        if db.__instance is None:
            db.__instance = object.__new__(cls)

            db.__instance.connection = sqlite3.connect(os.path.join(path_to_db, settings.DB_NAME))
            atexit.register(db.__instance.connection.close)

        return db.__instance

    @staticmethod
    def use(func):
        """ Wraps a specified function with connection/cursor interfaces.
        """
        @logger.log
        @wraps(func)
        def wrapped(*args, **kwargs):
            """Pass the wrapped function some required arguments for databse use.
            """
            connection = db().connection
            cursor = connection.cursor()
            func(connection, cursor, *args, **kwargs)

        return wrapped
