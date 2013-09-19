"""
Games are in localized eastern time.  Need to convert them to UTC
so that this batshit crazy bonkers shit stops. I hate time.

Why is time hard?
"""
import sys
import datetime
import pytz

from fadeben.lib.script import bootstrap
from fadeben.model import *
from fadeben.model.meta import Base
from fadeben.lib import dt

def convert_to_utc():
    games = Session.query(Game).all()

    for game in games:
        orig = game.game_time
        game.game_time = dt.utcfromlocal(game.game_time, pytz.timezone('America/New_York'))

        Session.add(game)

    Session.commit()
    print "{0} games converted to UTC".format(len(games))

def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'development.ini'

    bootstrap(config_file, '.')
    convert_to_utc()

if __name__ == '__main__':
    main()

