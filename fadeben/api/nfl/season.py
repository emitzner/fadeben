import logging

from unstdlib.standard import get_many

from fadeben.model import Session, Season, Game

__all__ = ['list', 'find', 'current', 'current_week', 'weeks_completed']

def list():
    """
    Returns a list of seasons.
    TODO: Add parameters
    """
    q = Session.query(Season)

    return q.all()

def find(**params):
    season = params['season']

    return Session.query(Season).filter(Season.number==season).one()
    
def current_week(**params):
    # Get the minimum week number that has 
    # games with a null home score
    # todo: what to return if season is over?
    season = params['season']

    game = _find_earliest_uncompleted_game(season)

    if game is None:
        raise ValueError

    return game.week

def weeks_completed(**params):
    """Returns the number of weeks that were completed in a given season.

    This function does not abide by playoff grouping.
    """
    season_id = params['season']

    game = _find_earliest_uncompleted_game(season_id)

    if game is None:
        # There are no games that have no score.  There's 2 possibilities:
        #  1 - this season doesn't exist at all.
        #  2 - this season is actually over.
        season = Session.query(Season).filter(Season.number==season_id).one()

        return season.num_total_weeks

    return game.week - 1

def _find_earliest_uncompleted_game(season_id):
    q = Session.query(Game)
    q = q.filter(Game.season_num==season_id)
    q = q.filter(Game.home_score==None)
    q = q.order_by(Game.week.asc())

    return q.first()

