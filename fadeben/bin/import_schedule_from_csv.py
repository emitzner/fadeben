import os
import sys
import datetime
import csv
import pytz

from fadeben.lib.script import bootstrap
from fadeben.model import Session, Game, Team
from fadeben.lib import dt

from fadeben import api
SEASON_NUMBER = 48

def find_team(name):
    team = Session.query(Team).filter(Team.name==name).one()
    return team

def import_games(filepath):
    with open(filepath, "r") as csvfile:
        r = csv.reader(csvfile)

        for row in r:
            if row[0] == "Week":
                continue

            home_team = find_team(row[5])
            away_team = find_team(row[3])
            dtime_concat = "2013" + " " + row[2] + " " + row[6]
            game_time_ny = datetime.datetime.strptime(dtime_concat, "%Y %B %d %I:%M %p")
            game_time = dt.utcfromlocal(game_time_ny, pytz.timezone("America/New_York"))

            game = Game()
            game.away_team = away_team
            game.home_team = home_team
            game.season_num = SEASON_NUMBER
            game.week = row[0]
            game.game_time = game_time

            Session.add(game)

        Session.commit()

def import_game(week, data):
    for game in data:
        home_team = find_team(game['home'])
        away_team = find_team(game['away'])
        game_time = datetime.datetime.fromtimestamp(game['date'])

        api.nfl.game.save(
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            game_time=game_time,
            season=SEASON_NUMBER,
            week=week,
            )

def run():
    path = os.path.abspath(os.getcwd())
    filepath = os.path.join(path, 'fadeben', 'sdata', 'season_48', 'schedule.csv')

    bootstrap('development.ini', path)

    import_games(filepath)

if __name__ == '__main__':
    run()
