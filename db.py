import sqlite3
import ya
import config
import json

class DB_Manager:
    def __init__(self, database_name: str):
        self.database = database_name


    def create_tables(self):
        con = sqlite3.connect(self.database)
        with con:
            con.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY NOT NULL,
                    prompt JSON NOT NULL
            )''')
            con.commit()


    def new_user(self, user_id: int,):
        messages = [
                {
                    'role':'system',
                    'text': '''
    ты бот задача которого поболтать с пользователем'''
                }
            ]
        prompt = ya.Ai(messages).get_prompt()
        #print(prompt)
        #print(type(prompt))
        con = sqlite3.connect(self.database)
        #print(prompt)
        prompt = json.dumps(prompt)
        #print(prompt)
        with con:
            con.execute(f'''
                INSERT INTO users (id, prompt) VALUES
                    (?,?)
            ''', (user_id, prompt))
            con.commit()

    def new_chat(self, user_id: int,):
        messages = [
                {
                    'role':'system',
                    'text': '''
    ты бот задача которого поболтать с пользователем. это - групповой чат. тут сообщения от разных пользователей.'''
                }
            ]
        prompt = ya.Ai(messages).get_prompt()
        con = sqlite3.connect(self.database)
        prompt = json.dumps(prompt)
        with con:
            con.execute(f'''
                INSERT INTO users (id, prompt) VALUES
                    (?,?)
            ''', (user_id, prompt))
            con.commit()

    def update(self, PK: int, prompt):
        con = sqlite3.connect(self.database)
        #print(prompt)
        prompt = json.dumps(prompt)
        #print(prompt)
        with con:
            con.execute(f'UPDATE users SET prompt = ? WHERE id = {PK}',(prompt,))
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
            return json.loads(cur.execute(f'SELECT prompt FROM users WHERE id = {PK}').fetchall()[0][0])

if __name__=="__main__":
    db = DB_Manager(config.path)
    db.create_tables()