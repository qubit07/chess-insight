import sqlite3
from game_importer import GameImporter
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Used sqlite version: %s" % (sqlite3.version))
    except Error as e:
        print(e)
    return conn

def get_opening_id(conn, eco):
    sql = ''' SELECT id  FROM insight_opening
              WHERE eco LIKE ? '''
    cur = conn.cursor()
    cur.execute(sql, eco)
    return cur.fetchone()

def create_game(conn, game):
    sql = ''' INSERT INTO insight_game(elo_mean,elo_diff,result,opening_id,timecontrol,timestamp,raw)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, game)
    conn.commit()
    return cur.lastrowid

def main():
    conn = create_connection(r"../db.sqlite3")
    importer = GameImporter()
    games = importer.get_games('resources/full_games.pgn')
    for game in games:
        opening_id = get_opening_id(conn, (game.eco,))
        if opening_id is not None:
            print("create game: %s" %(opening_id))
            create_game(conn, (game.elo_mean, game.elo_diff, game.result, opening_id[0], game.timecontrol, game.timestamp, game.raw))
    print("create games: %s" % (len(games)))

if __name__ == '__main__':
    main()
