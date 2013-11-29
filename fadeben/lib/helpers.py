"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
import datetime
import logging

from webhelpers.html.tags import *
from webhelpers.text import *

from webhelpers.pylonslib.flash import Flash as _Flash

from fadeben.config.serverconfig import ServerConfig

from fadeben.lib.util import irange

from pylons import app_globals as g

serverconfig = ServerConfig()
flash = _Flash()

log = logging.getLogger(__name__)

def prediction_result_class(user, game, prediction):
    if prediction:
        vote = prediction.prediction
    else:
        vote = None

    now = datetime.datetime.utcnow()
    if game.home_score is None or game.game_time > now:
        return ''

    spread_home_score = game.home_score + game.spread
    if (vote is True and (spread_home_score >= game.away_score)) \
            or (vote is False and (game.away_score >= spread_home_score)):
        return 'win'
    else:
        return 'loss'
                    
def show_prediction(user, game, prediction):
    now = datetime.datetime.utcnow()

    if (prediction is None) \
            or (user.id != prediction.user_id \
                    and game.game_time > now):
        return '-'

    if prediction.prediction is True:
        return game.home_team.abbr
    else:
        return game.away_team.abbr
            
def get_grouped_picks(mapper, season, member, start, end):
    tally = 0
    for i in xrange(start+1, end+1):
        tally += get_num_picks_for_week(mapper, season, member, i)

    log.debug("{0}: {1} {2}== {3}".format(member.id, start+1, end+1, tally))
    return tally

def row_color(i):
    return ['even', 'odd'][ i % 2 ]

def cycle(i, choices=None):
    if choices is None:
        choices = ['even', 'odd']

    return choices[ i % len(choices) ]

def show_spread(spread):
    return ("{0:.1f}".format(spread) if spread is not None else '-')

def game_result_class(team, game, ats=False):
    if not game.is_finished():
        return ''

    winner = game.winner(ats)

    if winner is None:
        return 'tie'
    elif winner == team.id:
        return 'win'
    else:
        return 'loss'
        
def show_record(record):
    return '{0} - {1} - {2}'.format(*record)

def get_playoff_count(season, current_week, user, m):
    """Returns the correct amount of playoff
    predictions the user has made this season.

    Combines all the number of weeks after season's
    num_weeks into one
    """
    log.debug("map: {0}".format(m))
    p_m = m[user]
    log.debug("um: {0}".format(p_m))
    regular_season_weeks = season.num_weeks
    count = 0
    raise Exception
    for i in range(regular_season_weeks+1, current_week+1):
        count += p_m[i]
    log.debug("count {0}".format(count))
    return 15

def get_num_picks_for_week(pick_map, season, member, week):
    """Get number of correct picks for a week for a user.

    TODO: Aggregate playoff amounts
    """
    return pick_map.get(member.id, {}).get(week, 0)

def week_name(season, week):
    return "Week {0}".format(week)

def show_money(amount):
    if amount < 0:
        return "-${0}".format(abs(amount))
    else:
        return "${0}".format(amount)
