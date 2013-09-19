import logging
import datetime

from collections import defaultdict

from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func, and_
from unstdlib.standard import get_many

from fadeben.model import Session, Season, Prediction, Game, User
from fadeben.api.nfl import season as season_api

log = logging.getLogger(__name__)

def list(**params):
    """
    :param user_id
    :param game_id
    :param week
    :param season
    """
    req = ['season']
    optional = ['user_id', 'game_id', 'week']
    season, user_id, game_id, week = get_many(params, req, optional)

    if not (user_id or game_id):
        raise ValueError("zomg")

    q = Session.query(Prediction)

    if game_id:
        q = q.filter(Prediction.game_id==game_id)
    else:
        q = q.join(Game)
        q = q.filter(Game.season_num==season)

        if week:
            q = q.filter(Game.week==week)

    if user_id:
        q = q.filter(Prediction.user_id==user_id)

    return q.all()

def save(**params):
    """
    :param user_id
    :param game_id
    :param prediction
    """

    user_id, game_id, prediction = get_many(params, [],
                                            ['user_id', 'game_id', 'prediction'])

    # Find the game.
    game = Session.query(Game).get(game_id)

    time_now = datetime.datetime.utcnow()
    if game.game_time < time_now:
        raise ValueError("You cannot make a prediction for this game anymore.")

    q = Session.query(Prediction)
    q = q.filter(Prediction.user_id==user_id)
    q = q.filter(Prediction.game_id==game_id)

    p = q.first()

    if not p:
        # Creating prediction...
        p = Prediction()
        p.user_id = user_id
        p.game_id = game_id

    p.prediction = prediction

    Session.add(p)
    Session.commit()

    return p

def find(**params):
    user_id, game_id = get_many(params, ['user_id', 'game_id'])

    q = Session.query(Prediction)
    q = q.filter(Prediction.user_id==user_id)
    q = q.filter(Prediction.game_id==game_id)

    return q.first()

def list_by_user(**params):
    """
    Returns a map of user_id -> game_ids -> predictions
    :param season: Season
    :param user_ids: List of user id's to grab
    :param game_ids: List of games to grab
    :param week (optional): week
    """

    season, user_ids, game_ids, week = get_many(params,
                                               ['season', 'user_ids'],
                                               ['game_ids', 'week'])

    q = Session.query(Prediction)
    #if week:
    #    q = q.join(Game)
    #    q = q.filter(Game.week==week)
    
    q = q.filter(Prediction.user_id.in_(user_ids))
    if game_ids:
        q = q.filter(Prediction.game_id.in_(game_ids))
    else:
        # need to join game, filter by season
        q = q.join(Game)
        q = q.filter(Game.season_num==season)
        if week:
            q = q.filter(Game.week==week)
        else:
            # todo, maybe not make this an else
            q = q.group_by(Game.week)
            log.debug("grouping by week")

    preds = q.all()

    m = defaultdict( dict )

    for p in preds:
        # Loop over each prediction.
        if game_ids or week:
            m[p.user_id][p.game_id] = p
        else:
            # group by week, not by game id
            m[p.user_id][p.game.week] = 1

    return m
    
def count_user_picks_raw(**params):
    """Returns a count of correct predictions
    by user id.

    This function does not group the playoff weeks.

    Thus if a season has 17 regular season weeks, and 4 playoff weeks,
    each player will have a count for 21 weeks.
    :param season
    :param user_ids
    :param week (optional)

    If week is provided, it will only return the correct amount
    for that week
    """

    season, user_ids, week = get_many(params,
                                      ['season', 'user_ids'],
                                      ['week'])

    q = _build_count_query(season, user_ids, week)

    if week:
        q = q.filter(Game.week==week)
        
    now = datetime.datetime.utcnow()
    q = q.filter(Game.game_time<=now)

    results = q.all()
    log.debug("results for season: {0}".format(results))

    # Loop through them all and make a mapping
    m = {}
    for r in results:
        m[r[0]] = r[1]

    if not m:
        # We need to return *something*
        m = {}
        for uid in user_ids:
            m[uid] = 0
        return m

    return m

def count_user_week_raw(**params):
    """returns a count of correct predictions, grouped by week for a season

    :param season
    :param user_ids
    """
    
    season, user_ids = get_many(params, ['season', 'user_ids'])

    q = _build_count_query(season, user_ids)
    q = q.add_column(Game.week)
    q = q.group_by(Game.week)
    results = q.all()
    
    m = defaultdict(dict)
    for r in results:
        # Game.week was added to the selected columns after the fact,
        # so it's actually the last queried column.
        # user -> week -> correct picks
        m[r[0]][r[2]] = r[1]

    return m

def count_user_week(**params):
    """Returns a count of correct prediction, grouped by week for a season.

    This function takes into account of playoff grouping, and thus
    there will only be season.num_weeks+1 weeks max returned per user.

    :param season
    :param user_ids
    """
    grouped_map = defaultdict(dict)
    # Step 1 - hydrate the actual season object, since we need num_weeks
    season_id, user_ids = get_many(params, ['season_id', 'user_ids'])

    season = Session.query(Season).filter(Season.number==season_id).one()

    # Step 2 - get the raw count.
    raw_map = count_user_week_raw(season=season_id, user_ids=user_ids)

    # Check the number of completed weeks.  If we're not in playoff territory
    # just return the raw map.
    completed_weeks = season_api.weeks_completed(season=season_id)

    if completed_weeks <= season.num_weeks:
        return raw_map

    # Step 3 - group the playoff weeks.
    for user_id in user_ids:
        # We're into playoff territory.  Copy
        # the results of the regular season weeks, and then aggregate
        # the playoff count.
        for i in xrange(1, season.num_weeks+1):
            grouped_map[ user_id ][i] = raw_map[ user_id ].get(i, 0)

        # Now, for the playoff weeks, we nee to aggregate.
        playoff_count = 0
        for i in xrange(season.num_weeks+1, completed_weeks+1):
            playoff_count += raw_map[user_id].get(i, 0)

        grouped_map[ user_id ][ season.num_weeks+1 ] = playoff_count

    return grouped_map

def find_unpredicted(**params):
    user_id, start_date, end_date = get_many(
        params,
        ['user_id', 'start_date', 'end_date']
        )

    q = Session.query(Game)
    q = q.filter(Game.game_time>=start_date)
    q = q.filter(Game.game_time<=end_date)
    games = q.all()
    
    missing = []
    # TODO: don't be an idiot about this.
    for game in games:
        # find their prediction
        p_q = Session.query(Prediction)
        p_q = p_q.filter(Prediction.user_id==user_id)
        p_q = p_q.filter(Prediction.game_id==game.id)

        pred = p_q.first()

        if pred is None:
            missing.append(game)

    return missing
    


def _build_count_query(season, user_ids, week=None):
    """This can be built off of"""
    q = Session.query(User.id, func.count(Prediction.user_id))
    q = q.filter(User.id.in_(user_ids))
    q = q.outerjoin(Prediction)
    q = q.join(Game, Prediction.game_id==Game.id)
    q = q.filter(Game.season_num==season)
    q = q.filter(Game.home_score!=None)

    if week:
        q = q.filter(Game.week==week)

    # Check for correct predictions
    correct_away = and_(Game.home_score + Game.spread <= Game.away_score, Prediction.prediction==False)
    correct_home = and_(Game.home_score + Game.spread >= Game.away_score, Prediction.prediction==True)
    correct_combined = or_(correct_away, correct_home)
    q = q.filter(correct_combined)
    q = q.group_by(User.id)
    return q
