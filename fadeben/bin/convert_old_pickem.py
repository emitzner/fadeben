import sys
import datetime
import os
import simplejson as json

from fadeben.lib.script import bootstrap
from fadeben.model import *
from fadeben.model.meta import Base

PICKEM_SEASON = 45
BACKUP_DATA_PATH = 'fadeben/sdata/bkup/'
USERS_FILE = 'users.json'
GAMES_FILE = 'games.json'
TEAMS_FILE = 'teams.json'
PREDICTIONS_FILE = 'predictions.json'

def reset():
    Base.metadata.drop_all(bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)

def create_season():
    season = Season()
    season.number = 45
    season.num_weeks = 17
    season.num_post_weeks = 4
    season.start = datetime.date(2011, 9, 9)
    season.end = datetime.date(2012, 2, 6)
    Session.add(season)
    #Session.commit()

def import_users():
    path = os.path.join(BACKUP_DATA_PATH, USERS_FILE)
    f = open(path)
    data = json.loads(f.read())
    for user in data:
        fields = user['fields']
        u = User()
        u.id = user['pk']
        u.username = fields['username']
        u.name = '{0} {1}'.format(fields['first_name'], fields['last_name'])
        u.password = 'blank'
        u.salt = 'blank'
        u.email = fields['email']
        Session.add(u)

def import_teams():
    path = os.path.join(BACKUP_DATA_PATH, TEAMS_FILE)
    f = open(path)
    data = json.loads(f.read())
    for team in data:
        fields = team['fields']
        t = Team()
        t.id = team['pk']
        t.name = fields['name']
        t.abbr = fields['abbreviation']
        t.conference = 1 # filler
        t.division = 1 # filler
        Session.add(t)

    f.close()

def parse_timestamp(timestamp):
    year, month, day = timestamp.split("-")

    return datetime.datetime(int(year), int(month), int(day))

def parse_datetime(t):
    date, time = t.split("T") # wtf django?
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')
    return datetime.datetime(int(year), int(month), int(day),
                             int(hour), int(minute), int(second))

def get_weeks():
    path = os.path.join(BACKUP_DATA_PATH, 'weeks.json')
    f = open(path)
    data = json.loads(f.read())
    weeks = []
    for d in data:
        w = {}
        fields = d['fields']
        w['start'] = parse_timestamp(fields['start_date'])
        w['end'] = parse_timestamp(fields['end_date'])
        w['number'] = d['pk']
        weeks.append(w)

    f.close()
    return weeks

def find_week_for_game(game, weeks):
    end_of_day_delta = datetime.timedelta(hours=23, minutes=59)
    for w in weeks:
        if game.game_time > w['start'] \
                and game.game_time <= (w['end'] + end_of_day_delta):
            return w['number']

    raise Exception("no week found for game")


def import_games():
    # The weeks need to be put into a data structure
    weeks = get_weeks()
    path = os.path.join(BACKUP_DATA_PATH, GAMES_FILE)
    f = open(path)
    data = json.loads(f.read())
    for game in data:
        fields = game['fields']
        g = Game()
        g.id = game['pk']
        g.season_num = PICKEM_SEASON
        
        g.home_team_id = fields['home_team']
        g.away_team_id = fields['away_team']
        g.spread = fields['spread']
        g.home_score = fields['home_score']
        g.away_score = fields['away_score']
        g.game_time = parse_datetime(fields['game_time'])
        g.week = find_week_for_game(g, weeks)

        Session.add(g)

def import_predictions():
    path = os.path.join(BACKUP_DATA_PATH, PREDICTIONS_FILE)
    f = open(path)
    data = json.loads(f.read())
    for pred in data:
        fields = pred['fields']
        p = Prediction()
        p.user_id = fields['user']
        p.game_id = fields['game']
        p.prediction = fields['prediction']
        Session.add(p)

def create_membership():
    for i in xrange(1, 6):
        m = Member()
        m.season_num = PICKEM_SEASON
        m.user_id = i
        Session.add(m)

def fix_jac():
    team = Session.query(Team).filter(Team.abbr=='JAC').first()

    if team:
        team.name = "Jacksonville Jaguars"
        Session.add(team)
        Session.commit()

def main():
    bootstrap('development.ini', '.')
    reset()
    create_season()
    import_users()
    import_teams()
    import_games()
    import_predictions()
    create_membership()

    Session.commit()
    fix_jac()

if __name__ == '__main__':
    main()
