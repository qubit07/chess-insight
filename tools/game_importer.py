import re
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

    def get_games(self, filepath):
        games = []
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                line = fp.readline()

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
                    self.raw = line.strip()
                    game = self.create_game_object()
                    games.append(game)

        return games;

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

    def create_game_object(self):
        self.elo_mean = self.calculate_elo_mean(self.white_elo, self.black_elo)
        self.elo_diff = self.calculate_elo_diff(self.white_elo, self.black_elo)
        timestamp = datetime.strptime(self.utc_date + '-' + self.utc_time,'%Y.%m.%d-%H:%M:%S')

        return (self.elo_mean, self.elo_diff, self.result, self.timecontrol, timestamp, self.raw)
