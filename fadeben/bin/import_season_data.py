import os
import sys
import datetime

import simplejson as json

from fadeben.lib.script import bootstrap
from fadeben.model import Session, Game, Team

from fadeben import api
SEASON_NUMBER = 47

def find_team(name):
    team = Session.query(Team).filter(Team.name==name).one()
    return team

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
    week = sys.argv[1]
    path = os.path.abspath(os.getcwd())
    filepath = os.path.join(path, 'fadeben', 'sdata', 'w{0}.json'.format(week))

    bootstrap('development.ini', path)

    data = open(filepath, 'r').read()

    data = json.loads(data)
    
    import_game(week, data)

if __name__ == '__main__':
    run()
