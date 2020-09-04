import sqlite3
from opening_importer import OpeningImporter
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Used sqlite version: %s" % (sqlite3.version))
    except Error as e:
        print(e)
    return conn

def create_opening_system(conn, opening_system):
    sql = ''' INSERT INTO insight_openingsystem(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, opening_system)
    conn.commit()
    return cur.lastrowid

def get_opening_system_id(conn, name):
    sql = ''' SELECT id  FROM insight_openingsystem
              WHERE name LIKE ? '''
    cur = conn.cursor()
    cur.execute(sql, name)
    return cur.fetchone()

def create_opening(conn, opening):
    sql = ''' INSERT INTO insight_opening(name,eco,opening_system_id,moves)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, opening)
    conn.commit()
    return cur.lastrowid

def main():
    conn = create_connection(r"../db.sqlite3")
    opening_importer = OpeningImporter()
    opening_systems = opening_importer.get_opening_systems('resources/chess_eco_codes.json')
    for opening_system in opening_systems:
        create_opening_system(conn, (opening_system,))

    openings = opening_importer.get_openings('resources/chess_eco_codes.json')
    for opening in openings:
        opening_system_id = get_opening_system_id(conn, (opening.opening_system,))
        opening.opening_system = opening_system_id[0]
        create_opening(conn, (opening.name, opening.eco, opening.opening_system, opening.moves))
    print("create opening sytems: %s" % (len(opening_systems)))
    print("create openings: %s" % (len(openings)))



if __name__ == "__main__":
    main()
