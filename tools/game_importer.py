import re
from datetime import datetime
from game import Game

class GameImporter:

    def __init__(self):
        self.games = []

    def get_games(self, filepath):
        with open(filepath) as fp:
            line = fp.readline()
            game = Game()
            while line:
                line = fp.readline()

                if self.is_regex_in_line(line, 'WhiteElo'):
                    game.white_elo = int(self.get_line_value(line, 'WhiteElo'))

                if self.is_regex_in_line(line, 'BlackElo'):
                    game.black_elo = int(self.get_line_value(line, 'BlackElo'))

                if self.is_regex_in_line(line, 'UTCDate'):
                    game.utc_date = self.get_line_value(line, 'UTCDate')

                if self.is_regex_in_line(line, 'UTCTime'):
                    game.utc_time = self.get_line_value(line, 'UTCTime')

                if self.is_regex_in_line(line, 'ECO'):
                    game.eco = self.get_line_value(line, 'ECO')

                if self.is_regex_in_line(line, 'Result'):
                    game.result = self.get_line_value(line, 'Result')

                if self.is_regex_in_line(line, 'TimeControl'):
                    game.timecontrol = self.get_line_value(line, 'TimeControl')

                if self.is_line_start_with(line, '1.'):
                    game.raw = line.strip()
                    game.elo_mean = self.calculate_elo_mean(game.white_elo, game.black_elo)
                    game.elo_diff = self.calculate_elo_diff(game.white_elo, game.black_elo)
                    timestamp = datetime.strptime(game.utc_date + '-' + game.utc_time,'%Y.%m.%d-%H:%M:%S')
                    game.timestamp = timestamp
                    self.games.append(game)
                    game = Game()

        return self.games;

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
