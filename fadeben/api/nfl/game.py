import logging
import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from unstdlib.standard import get_many

from fadeben.model import Session, Season, Game

log = logging.getLogger(__name__)

def list(**params):
    """Find all the games or something like that

    :param season: The season to get the games from
    :param week: The week, if season is specified
    :param team (optional): Games for a particular team
    :param completed (optional): Only games that are completed
    :param not_started (optional): Only games that haven't started yet
    :param in_progress (optional): Only games that have started but don't have a score logged
    :param playoffs (optional): Return the playoff games for this season.  Cannot be used with 'week'
    """
    #params['season'] = 47
    optional = ['week', 'team', 'completed', 'not_started', 'in_progress', 'playoffs', 'no_spread']
    season, week, team, completed, not_started, in_progress, playoffs, no_spread = get_many(params, ['season'], optional)

    q = Session.query(Game)

    q = q.options(joinedload('away_team'),
                  joinedload('home_team')
                  )
    
    if season:
        q = q.filter(Game.season_num==season)

    if week:
        q = q.filter(Game.week==week)

    elif playoffs:
        # HACK: if we ever have seasons with more than 17 regular season
        # weeks, this won't work.  But oh well. It doesn't seem worth it to
        # query the database everytime this is called for something that isn't
        # supported at all.
        q = q.filter(Game.week>17)

    if team:
        q = q.filter(or_(
                Game.away_team_id==team,
                Game.home_team_id==team
                ))

    if completed:
        q = q.filter(Game.home_score!=None)
    elif not_started:
        time_now = datetime.datetime.utcnow()
        q = q.filter(Game.game_time>time_now)
    elif in_progress:
        time_now = datetime.datetime.utcnow()
        q = q.filter(Game.game_time<time_now)
        q = q.filter(Game.home_score==None)
    elif no_spread:
        q = q.filter(Game.spread==None)

    q = q.order_by(Game.week)
    q = q.order_by(Game.game_time)

    return q.all()

def save(**params):
    """Save a game
    :param game_id (optional): If game_id is provided,
           it will edit the existing game.
           Otherwise, it will create one
    :param season: Season
    :param week: The week the game is to be played in
    :param away_team_id: Away team
    :param home_team_id: Home team
    :param away_score: Away team score
    :param home_score: Home team score
        Note - if any of *_score is provided,
        they both must be provided
    :param game_time: Datetime of the start of the game
    :param spread (optional): The spread of the game
    """
    req = ['season', 'week', 'home_team_id', 'away_team_id',
           'game_time']
    opt = ['game_id', 'home_score', 'away_score', 'spread']
    season, week, ht_id, at_id, gt, g_id, h_s, a_s, spread = \
        get_many(params, required=req, optional=opt)

    if g_id:
        is_edit = True
        game = Session.query(Game).filter(Game.id==g_id).one()
    else:
        is_edit = False
        log.debug("Creating new game")
        game = Game()

    game.season_num = season
    game.week = week
    game.game_time = gt
    game.spread = spread
    game.home_team_id = ht_id
    game.away_team_id = at_id
    game.home_score = h_s
    game.away_score = a_s

    Session.add(game)
    Session.commit()
    return game

def update(**params):
    """
    This is to simplify just updating the scores
    and spreads of a game
    """
    game_id, home_score, away_score, spread = \
        get_many(params, ['game_id'], ['home_score', 'away_score', 'spread'])

    game = Session.query(Game).filter(Game.id==game_id).one()

    game.home_score = home_score
    game.away_score = away_score

    if spread is not None:
        game.spread = spread

    Session.add(game)
    Session.commit()
    return game
    
def find(**params):
    """Find a specific game"""
    game_id = params['game_id']
    q = Session.query(Game)
    q = q.filter(Game.id==game_id)
    return q.one()

