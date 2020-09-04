import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Used sqlite version: %s" % (sqlite3.version))
    except Error as e:
        print(e)
    return conn

def create_user(conn, user):
    sql = ''' INSERT INTO insight_user(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def main:
    conn = create_connection(r"../db.sqlite3")
    user = ('easyjunker',)
    user_id = create_user(conn, user)
    print("create user: %s" % (user_id))

if __name__ == "__main__":
    main()
