"""
If there's games today, we want to remind the user to pick
the winner, if they haven't already done so.
"""
import sys
import datetime
import logging
import os

from fadeben.lib.script import bootstrap
from fadeben.model import *
from fadeben.model.meta import Base
from fadeben.lib import dt
from fadeben import api

from pylons import app_globals as g

log = logging.getLogger("fadeben.reminder")

def convert_to_utc():
    games = Session.query(Game).all()

    for game in games:
        orig = game.game_time
        game.game_time = dt.utcfromlocal(game.game_time, pytz.timezone('America/New_York'))

        Session.add(game)

    Session.commit()
    print "{0} games converted to UTC".format(len(games))

def remind_users():
    current_season = g.serverconfig.get_value('current_season')

    users = api.pickem.member.list(season=current_season)

    t = datetime.datetime.utcnow()
    
    start_date = datetime.datetime.utcnow()

    end_date = start_date + datetime.timedelta(
        hours=23,
        minutes=59
        )

    log.info("Scanning for games without predictions between {0} and {1}".format(
            start_date, end_date))

    for user in users:
        # send them some shit yo.
        unpredicted_games = api.pickem.prediction.find_unpredicted(
            user_id=user.id, 
            start_date=start_date,
            end_date=end_date
            )

        if not unpredicted_games:
            log.info("User {0} has no unpredicted games for this time period of {1}-{2}".format(user.id, start_date, end_date))
            continue

        api.pickem.member.send_reminder(
            user_id=user.id,
            games=unpredicted_games)

    return

def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'development.ini'

    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    bootstrap(config_file, proj_dir)
    remind_users()

if __name__ == '__main__':
    main()

