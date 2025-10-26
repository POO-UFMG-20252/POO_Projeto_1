import sqlite3
DB_NAME = "database.db"
class autenticador:

    @staticmethod
    def signup(user,password):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO t_auth (user,password) VALUES (?, ?)", (user, password))
            con.commit()
        
    @staticmethod
    def login(user,password):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("SELECT * from t_auth WHERE user=? AND password=?", (user, password))
            con.commit()
            return cur.fetchone() is not None#retorna true se bater e false se n
        