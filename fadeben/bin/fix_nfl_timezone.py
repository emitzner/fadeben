"""
So, apparently NFL.com thinks that America/New_York is the same thing
as EST.  It's not, so all the games before nov 4th got 
parsed as an hour later than they actually are.  Nice going, NFL.
"""
import sys
import datetime

from fadeben.lib.script import bootstrap
from fadeben.model import *
from fadeben.model.meta import Base

def fix_times():
    cutoff = datetime.datetime(2012, 11, 4, 0,0,0)
    # find all the games before november 4th
    q = Session.query(Game)
    q = q.filter(Game.season_num==47)
    q = q.filter(Game.id>271) # that game was already fixed
    q = q.filter(Game.week<10) # that's the cutoff week, there's some straggling games
    q = q.filter(Game.game_time<cutoff)

    games = q.all()

    # Now, we need to fix these games.
    # ideally i'd rather do a bulk update, but there's a few issues
    # datetimes are stored as strings in sqlite (the main db, as of now)
    # and i honestly just don't know how to do bulk updates with sqla orm, and
    # since at the time of this writing it's only 119 affected games, i don't really
    # care so much
    delta = datetime.timedelta(hours=-1)
    for game in games:
        game.game_time = game.game_time + delta
        Session.add(game)

    Session.commit()

    print "{0} games updated".format(len(games))

def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'development.ini'

    bootstrap(config_file, '.')
    fix_times()

if __name__ == '__main__':
    main()

