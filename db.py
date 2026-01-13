import sqlite3
def connect():
    con = sqlite3.connect("users.db")
    return con

def get_users(con, table):
    curs = con.cursor()
    res = curs.execute(f"SELECT name FROM sqlite_master WHERE name = '{table}'")
    if len(res.fetchall()) == 0:
            curs.execute(f"CREATE TABLE {table} (name, publickey, privkey)")
    res = curs.execute(f"SELECT name FROM {table}")
    return res.fetchall()

def add_user(con, data, table):
    curs = con.cursor()
    curs.execute(f"INSERT INTO {table} (name, publickey, privkey) VALUES (?, ?, ?)", data)
    con.commit()

def del_user(con, username, table):
    curs = con.cursor()
    print(username)
    res = curs.execute(f"DELETE FROM {table} WHERE name = ?",username)
    print(f"DELETE FROM {table} WHERE name = ?",username)
    print(res.fetchall())
    con.commit()
    