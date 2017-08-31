import sqlite3

from functools import wraps

from logger import logger


class db:

    __instance = None
    def __new__(cls, path_to_db=None):
        if db.__instance is None:
            db.__instance = object.__new__(cls)
            db.__instance.connection = sqlite3.connect(path_to_db)
        return db.__instance

    @staticmethod
    def use(func):
        @logger.log
        @wraps(func)
        def wrapped(*args, **kwargs):
            connection = db().connection
            cursor = connection.cursor()
            func(connection, cursor, *args, **kwargs)
            db().connection.close()

        return wrapped
