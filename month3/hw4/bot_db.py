import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("menu.sqlite3")
    cursor = db.cursor()

    if db:
        print("Data base connected.")

    db.execute("CREATE TABLE IF NOT EXISTS menu"
               "(photo TEXT,"
               "name TEXT PRIMARY KEY, description TEXT, price INTEGER)")
    db.commit()


async def sql_command_ins(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES "
                       "(?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(name):
    cursor.execute("DELETE FROM menu WHERE name == ?", (name,))
    db.commit()