import sqlite3
def connect():
    con = sqlite3.connect("users.db")
    return con

def get_users(con, table):
    curs = con.cursor()
    res = curs.execute(f"SELECT name FROM sqlite_master WHERE name = '{table}'")
    if len(res.fetchall()) == 0:
            curs.execute(f"CREATE TABLE {table}(name, publickey, privkey)")
    res = curs.execute(f"SELECT name FROM {table}")
    return res.fetchall()

def add_user():
    ...

def del_user(con, username, table):
    curs = con.cursor()
    params = (str(username),)
    res = curs.execute(f"DELETE FROM {table} WHERE name = ?",params)
    con.commit()
    