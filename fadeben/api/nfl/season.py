import logging

from unstdlib.standard import get_many

from fadeben import model

__all__ = ['list', 'find', 'current', 'current_week', 'weeks_completed']

class Season(object):
    def __init__(self, season):

        if isinstance(season, int):
            # passed in a season id
            self.season_id = season
            self.season = None
        elif isinstance(season, model.Season):
            self.season = season
            self.season_id = season.number
        else:
            raise TypeError("")

        self._earliest_uncompleted_game = None
        self._games = []

    def _get_season(self):
        if self.season:
            return self.season
        else:
            return model.Session.query(model.Season).get(self.season_id)

    def get_current_week(self):
        game = self._find_earliest_uncompleted_game()

        if game is None:
            return None

        return game.week

    def has_season_finished(self):
        return (self.get_current_week() is None)

    def has_season_begun(self):
        
        return True

    def is_week_finished(self, week_number):
        return (self.get_current_week() > week_number)

    def _find_earliest_uncompleted_game(self):
        if self._earliest_uncompleted_game is None:
            q = model.Session.query(model.Game)
            q = q.filter(model.Game.season_num==self.season_id)
            q = q.filter(model.Game.home_score==None)
            q = q.order_by(model.Game.week.asc())

            self._earliest_uncompleted_game = q.first()

        return self._earliest_uncompleted_game

def list():
    """
    Returns a list of seasons.
    TODO: Add parameters
    """
    q = model.Session.query(model.Season)

    return q.all()

def find(**params):
    season = params['season']

    return model.Session.query(model.Season).filter(model.Season.number==season).one()
    
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
        season = model.Session.query(model.Season).filter(model.Season.number==season_id).one()

        return season.num_total_weeks

    return game.week - 1

def _find_earliest_uncompleted_game(season_id):
    q = model.Session.query(model.Game)
    q = q.filter(model.Game.season_num==season_id)
    q = q.filter(model.Game.home_score==None)
    q = q.order_by(model.Game.week.asc())

    return q.first()

