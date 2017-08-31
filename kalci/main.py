import click
import os
import sqlite3

from database import db


@db.use
def do_stuff(conn, cursor):
    try:
        cursor.execute('''
                        create table tasks
                        (task text, completed integer, priority integer)
                       ''')
    except sqlite3.OperationalError as e:
        pass

    print('I did a thing!')

@click.command()
@click.option('--path-to-db',
              default=os.path.join(os.getcwd(), 'kalci.sqlite3'),
              help='Location of kalci sqlite3 data...')
def main(path_to_db):
    db(path_to_db)

    do_stuff()


if __name__ == '__main__':
    main()
