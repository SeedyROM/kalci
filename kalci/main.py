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
              default=os.path.join(os.getcwd(), 'kalci.sqlite3'),
              help='Location of kalci sqlite3 data...')
def main(path_to_db):
    db(path_to_db)

    do_stuff()
    do_more_stuff()


if __name__ == '__main__':
    main()
