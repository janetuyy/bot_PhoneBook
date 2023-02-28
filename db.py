import sqlite3
conn = sqlite3.connect(r'D:/bot/notes.db',check_same_thread=False)
cur = conn.cursor()

flag_add = False
flag_get = False
flag_delete = False


def init():
    cur.execute("""CREATE TABLE IF NOT EXISTS notes(
        chat_id INTEGER,
        name TEXT,
        number INTEGER,
        note TEXT);
    """)
    conn.commit()


def insert(id,name, number, note):
    init()
    cur.execute(f'INSERT INTO notes VALUES ({id},"{name}",{number},"{note}")')
    conn.commit()
    


def select(id):
    init()
    cur.execute(f'SELECT * FROM notes WHERE chat_id = {id}')
    return cur.fetchall()

def get(id,name):
    init()
    cur.execute(f'SELECT * FROM notes WHERE name = "{name}" AND chat_id = {id}')
    return cur.fetchone()

def delete(id,name):
    init()
    cur.execute(f'DELETE FROM notes WHERE name = "{name}" AND chat_id = {id}')
    conn.commit()

def check(id,name):
    init()
    cur.execute(f'SELECT * FROM notes WHERE name = "{name}" AND chat_id = {id}')
    return (cur.fetchone() != None)