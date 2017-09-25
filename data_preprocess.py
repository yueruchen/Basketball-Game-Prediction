#-*- coding: utf-8 -*-

import random
import numpy as np

__all__ = ['MatchData']


def remove_duplicate(data):
    pass


def load_team_data():

    team_data = []

    with open('data/teamData.csv', 'r') as open_file:
        lines = open_file.readlines()
    lines = lines[1:]
    # 6 9 12

    def get_num(_str):
        if len(_str) == 0:
            return 0.0
        _rec = _str.replace('%','')
        return float(_rec)

    for line in lines:
        info = [get_num(x) for x in line.split(',')]
        team_data.append(info)
    return team_data


def load_competitions():
    """
    Load Comepetions
    Competition: [(Away, Home, Away_Ago_Win, Away_Ago_Lose, Home_Ago_Win, Home_Ago_Lose, Away_Score, Home_Score)]
    """

    data = []
    with open('data/matchDataTrain.csv') as open_file:
        lines = open_file.readlines()

    def get_record(rec_str):
        rec_str = rec_str.replace('胜', ',')
        rec_str = rec_str.replace('负', ',')
        records = map(int, rec_str.split(',')[:-1])

        return records

    for line in lines[1:]:
        elements = line.split(',')
        away = int(elements[0])
        home = int(elements[1])

        away_ago = get_record(elements[2])
        home_ago = get_record(elements[3])

        score = map(int, elements[4].split(':'))

        parts = [away, home] + away_ago + home_ago + score

        data.append(parts)

    return data


class TeamData(object):

    def __init__(self):
        self._team = dict()

    def get_team(self, id):
        return self._team[id]

    def process(self):

        team_data = load_team_data()
        current_arr = []
        current_team = 0
        for member in team_data:
            if member[0] != current_team:
                self._team[current_team] = current_arr
                current_arr = []
                current_team += 1
            current_arr.extend(member[2:])

    def test(self):

        for key in self._team.keys():
            print("KEY: %s NUMS: %s CONTENT: %s" %(key, len(self._team[key]), self._team[key]))


class MatchData(object):

    def __init__(self, testing_size):
        self.data = load_competitions()
        random.shuffle(self.data)
        self.current_index = 0
        self.testing_size = testing_size

    def roll_data(self):
        """
        :description: cross-validation shuffle data when the index > size 
        """
        if self.current_index > len(self.data):
            self.current_index = 0
            random.shuffle(self.data)
        self.testing_data = self.data[self.current_index:self.current_index+self.testing_size]
        self.training_data = self.data[:self.current_index]+self.data[self.current_index+self.testing_size:]
        self.current_index += self.testing_size

    def get_train_data(self):
        self.roll_data()
        return self.training_data

    def get_test_data(self):
        return self.testing_data

    def dump_matches_to_file(self, file_dir):

        csv_line = 'away,home,away_ago_win,away_ago_lose,home_ago_win,home_ago_lose,score_away,score_home\n'
        with open(file_dir+'train.csv', 'w+') as f:
            f.write(csv_line)
            for match in self.training_data:
                line = ','.join(['%s' % x for x in match])
                line += '\n'
                f.write(line)

        with open(file_dir+'test.csv', 'w+') as f:
            f.write(csv_line)
            for match in self.testing_data:
                line = ','.join(['%s' % x for x in match])
                line += '\n'
                f.write(line)


def test_load_competitions():

    data = load_competitions()
    print(data[1:10])


def test_match_data():

    s = MatchData(1000)
    s.roll_data()
    s.dump_matches_to_file('data/')


def test_team_data():

    s = TeamData()
    s.process()


if __name__ == '__main__':

    test_team_data()











