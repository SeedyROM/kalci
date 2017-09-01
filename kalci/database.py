import atexit
import sqlite3
import os

import settings

from functools import wraps

from logger import logger


class db:
    __instance = None
    def __new__(cls, path_to_db=settings.DATA_PATH):
        if db.__instance is None:
            db.__instance = object.__new__(cls)

            db.__instance.connection = sqlite3.connect(os.path.join(path_to_db, settings.DB_NAME))
            atexit.register(db.__instance.connection.close)
            
        return db.__instance

    @staticmethod
    def use(func):
        @logger.log
        @wraps(func)
        def wrapped(*args, **kwargs):
            connection = db().connection
            cursor = connection.cursor()
            func(connection, cursor, *args, **kwargs)

        return wrapped
