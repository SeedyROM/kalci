"""The main kalci module, let's loaded first.
"""
import click
import os
import sqlite3

from . import settings
from .database import db


@db.use
def do_stuff(conn, cursor):
    """Test function.
    """
    try:
        cursor.execute('''
                        create table tasks
                        (task text, completed integer, priority integer)
                       ''')
    except sqlite3.OperationalError as e:
        cursor.execute('''
                        insert into tasks (task, completed, priority)
                        values ("I mean very nice person! Don\'t be mean to yourself.", 0, 2)
                       ''')

    conn.commit()
    print('I did a thing!')

@db.use
def do_more_stuff(conn, cursor):
    """Test function.
    """
    tasks = cursor.execute('select rowid, task, completed, priority from tasks').fetchall()
    print(tasks)


@click.command()
@click.option('--path-to-db',
              default=settings.DATA_PATH,
              help='Location of kalci sqlite3 data...')
def main(path_to_db):
    """Kalci's first point of execution, all the magic happens here.
    """

    #
    # Try to make our hidden data directory.
    #
    try:
        if not os.path.exists(settings.DATA_PATH):
            os.makedirs(settings.DATA_PATH)
    except OSError as e:
        print(f'Failed to create data directory...: {e}')
        exit(-1)
    #
    # End trying to create hidden data.
    #
    
    # Create the instance of our db singleton.
    db(path_to_db)

    # Test stuff.
    do_stuff()
    do_more_stuff()

# Execute our code.
if __name__ == '__main__':
    main()
