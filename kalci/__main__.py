"""The main kalci module, it get's loaded first.
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

def test_urwid(terminal_colors):
    import urwid

    def exit_on_q(key):
        if key.casefold() == 'q':
            raise urwid.ExitMainLoop()

    palette = [
        ('banner', '', '', '', '#ffa', '#60d'),
        ('streak', '', '', '', 'g50', '#60a'),
        ('inside', '', '', '', 'g38', '#808'),
        ('outside', '', '', '', 'g27', '#a06'),
        ('bg', '', '', '', 'g7', '#d06'),]

    placeholder = urwid.SolidFill()
    loop = urwid.MainLoop(placeholder, palette, unhandled_input=exit_on_q)
    loop.screen.set_terminal_properties(colors=256 if terminal_colors else 16)
    loop.widget = urwid.AttrMap(placeholder, 'bg')
    loop.widget.original_widget = urwid.Filler(urwid.Pile([]))

    div = urwid.Divider()
    outside = urwid.AttrMap(div, 'outside')
    inside = urwid.AttrMap(div, 'inside')
    txt = urwid.Text(('banner', u" KalCI == Here For U "), align='center')
    streak = urwid.AttrMap(txt, 'streak')
    pile = loop.widget.base_widget # .base_widget skips the decorations
    for item in [outside, inside, streak, inside, outside]:
        pile.contents.append((item, pile.options()))

    try:
        loop.run()
    except KeyboardInterrupt:
        pass


@click.command()
@click.option('--path-to-db',
              default=settings.DATA_PATH,
              help='Location of kalci sqlite3 data...')
@click.option('--terminal-colors/--no-terminal-colors',
               default=True)
def main(path_to_db, terminal_colors):
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

    # Test interface code.
    test_urwid(terminal_colors)

    # Test db stuff.
    do_stuff()
    do_more_stuff()

# Execute our code.
if __name__ == '__main__':
    main()
