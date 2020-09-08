import re
import sqlite3
from sqlite3 import Error
from datetime import datetime

class GameImporter:

    def __init__(self):
        self.white_elo = 0
        self.black_elo = 0
        self.elo_mean = 0
        self.elo_diff = 0
        self.utc_date = ''
        self.utc_time = ''
        self.variant = ''
        self.eco = ''
        self.raw = ''
        self.timecontrol = ''
        self.result = ''

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Used sqlite version: %s" % (sqlite3.version))
        except Error as e:
            print(e)
        return conn

    def get_opening_id(self, conn, eco):
        sql = ''' SELECT id  FROM insight_opening
                  WHERE eco LIKE ? '''
        cur = conn.cursor()
        cur.execute(sql, eco)
        return cur.fetchone()

    def create_game(self, conn, game):
        sql = ''' INSERT INTO insight_game(elo_mean,elo_diff,result,opening_id,timecontrol,timestamp,raw)
                  VALUES(?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, game)
        conn.commit()
        return cur.lastrowid

    def create_games(self, conn, filepath):
        with open(filepath) as fp:
            count = 0
            for line in fp:
                if self.is_regex_in_line(line, 'WhiteElo'):
                    self.white_elo = int(self.get_line_value(line, 'WhiteElo'))

                if self.is_regex_in_line(line, 'BlackElo'):
                    self.black_elo = int(self.get_line_value(line, 'BlackElo'))

                if self.is_regex_in_line(line, 'UTCDate'):
                    self.utc_date = self.get_line_value(line, 'UTCDate')

                if self.is_regex_in_line(line, 'UTCTime'):
                    self.utc_time = self.get_line_value(line, 'UTCTime')

                if self.is_regex_in_line(line, 'ECO'):
                    self.eco = self.get_line_value(line, 'ECO')

                if self.is_regex_in_line(line, 'Result'):
                    self.result = self.get_line_value(line, 'Result')

                if self.is_regex_in_line(line, 'TimeControl'):
                    self.timecontrol = self.get_line_value(line, 'TimeControl')

                if self.is_line_start_with(line, '1.'):
                    print("create game: %s" %(count))
                    count =  count+1;
                    self.raw = line.strip()
                    self.elo_mean = self.calculate_elo_mean(self.white_elo, self.black_elo)
                    self.elo_diff = self.calculate_elo_diff(self.white_elo, self.black_elo)
                    timestamp = datetime.strptime(self.utc_date + '-' + self.utc_time,'%Y.%m.%d-%H:%M:%S')
                    self.timestamp = timestamp
                    opening_id = self.get_opening_id(conn, (self.eco,))
                    if opening_id is not None:
                        self.create_game(conn, (self.elo_mean, self.elo_diff, self.result, opening_id[0], self.timecontrol, self.timestamp, self.raw))


    def is_regex_in_line(self, line, regex):
        if regex in line:
            return True
        else:
            return False

    def get_line_value(self, line, regex):
        quoted = re.compile('"[^"]*"')
        for value in quoted.findall(line):
            return value.strip('"')

    def is_line_start_with(self, line, regex):
        if line.startswith(regex):
            return True
        else:
            return False

    def calculate_elo_mean(self, white_elo, black_elo):
        return (white_elo + black_elo) /2;

    def calculate_elo_diff(self, white_elo, black_elo):
        return abs(white_elo - black_elo) ;

def main():
    importer = GameImporter()
    conn = importer.create_connection(r"../db.sqlite3")
    importer.create_games(conn,'resources/full_games.pgn')

if __name__ == '__main__':
    main()
