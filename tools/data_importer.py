import sqlite3
from eco_importer import EcoImporter
from game_importer import GameImporter
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)

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

def create_opening(conn, opening):
    sql = ''' INSERT INTO insight_opening(name,eco,moves)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, opening)
    conn.commit()
    return cur.lastrowid

def create_game(conn, game):
    sql = ''' INSERT INTO insight_game(elo_mean,elo_diff,result,timecontrol,timestamp,raw)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, game)
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    conn = create_connection(r"../db.sqlite3")
    user = ('easyjunker',)
    #user_id = create_user(conn, user)
    #print("create user: %s" % (user_id))

    eco_importer = EcoImporter()
    ecos = eco_importer.get_ecos('resources/chess_eco_codes.json')
    for eco in ecos:
        create_opening(conn,eco)
    print("create openings: %s" % (len(ecos)))


    importer = GameImporter()
    games = importer.get_games('resources/games.pgn')
    print("create games: %s" % (len(games)))
