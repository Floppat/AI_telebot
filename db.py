import sqlite3
import json

from config import path


class DB_Manager:
    def __init__(self, database_name: str):
        self.database = database_name

    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY NOT NULL,
                    history JSON NOT NULL
            )''')
            con.commit()

    def new_id(self, user_id: int, id_type):
        if id_type == 'user':
            text = 'ты бот задача которого поболтать с пользователем'
        elif id_type == 'chat':
            text = 'ты бот задача которого поболтать с пользователем. это - групповой чат. тут сообщения от разных пользователей.'
        else:
            print('type error')
            return
        messages = [{'role':'system', 'text': text}]
        con = sqlite3.connect(self.database)
        history = json.dumps(messages)
        with con:
            con.execute(f' INSERT INTO users (id, history) VALUES (?,?)', (user_id, history))
            con.commit()

    def update(self, PK: int, history):
        con = sqlite3.connect(self.database)
        history = json.dumps(history)
        with con:
            con.execute(f'UPDATE users SET history = ? WHERE id = {PK}',(history,))
            con.commit()
        return 'успешно изменено'
    
    def delete(self, PK: int):
        con = sqlite3.connect(self.database)
        with con:
            con.execute(f'DELETE FROM users WHERE id = {PK}')
        return 'успешно удалено'

    def read(self, PK: int):
        con = sqlite3.connect(self.database)
        with con:
            cur = con.cursor()
            return json.loads(cur.execute(f'SELECT history FROM users WHERE id = {PK}').fetchall()[0][0])
        
if __name__=="__main__":
    db = DB_Manager(path)
    db.create_tables()
