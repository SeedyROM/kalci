import click
import os
import sqlite3

import settings

from database import db


@db.use
def do_stuff(conn, cursor):
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
    tasks = cursor.execute('select rowid, task, completed, priority from tasks').fetchall()
    print(tasks)


@click.command()
@click.option('--path-to-db',
              default=settings.DATA_PATH,
              help='Location of kalci sqlite3 data...')
def main(path_to_db):
    try:
        if not os.path.exists(settings.DATA_PATH):
            os.makedirs(settings.DATA_PATH)
    except OSError as e:
        print(f'Failed to create data directory...: {e}')
        exit(-1)

    db(path_to_db)

    do_stuff()
    do_more_stuff()


if __name__ == '__main__':
    main()
