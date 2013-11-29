import logging

from sqlalchemy.orm import joinedload
from unstdlib.standard import get_many
from pylons import config

from fadeben.model import Session, Team, Game, Season

from fadeben.api.nfl import game as api_game

log = logging.getLogger(__name__)

def list(**params):
    """Return a list of NFL teams.
    """
    q = Session.query(Team)

    return q.all()

def find(**params):
    """Find a specific team.
    """

    team_id, team_abbr = get_many(params, [], optional=['team_id', 'team_abbr'])

    # Need either team_id or team_abbr specified.
    if not (team_id or team_abbr):
        raise KeyError("One of 'team_id' or 'team_abbr' must be provided")

    q = Session.query(Team)

    if team_id:
        q = q.filter(Team.id==team_id)
    else:
        q = q.filter(Team.abbr==team_abbr)

    return q.one()
    
def get_record(**params):
    """
    Get the record for a team
    :param team_id
    :param games: the list of games to calculate the record for
    :param ats: Whether or not to calculate this against the spread

    This will get updated in the future to support getting
    records against conferences, all time, etc.  For now,
    this will suffice.
    """
    team_id, games, ats = get_many(params, ['team_id', 'games'], ['ats'])
    
    record = [0, 0, 0]
    for game in games:
        if game is None or not game.is_finished():
            continue

        home_score = game.home_score

        if ats:
            home_score += game.spread
    
        if (team_id == game.home_team_id and home_score > game.away_score) \
                or (team_id == game.away_team_id and home_score < game.away_score):
            # win
            record[0] += 1
        elif game.away_score == home_score:
            # loss
            record[2] += 1
        else:
            # tie
            record[1] += 1

    return tuple(record)

def get_record_by_team(**params):
    """
    Returns a map of team -> record
    """

    team_ids = params['team_ids']

    record_map = {}

    for team_id in team_ids:
        record_map[team_id] = get_record(team_id=team_id)

    return record_map

def get_games(**params):
    """
    Returns a list of games for the team for the season provided.
    Will have a null entry for the bye week.
    """
    team_id, season_id = get_many(params, ['team_id', 'season_id'])

    # Get the season so that we can do some parsing
    season = Session.query(Season).filter(Season.number==season_id).one()

    games = api_game.list(season=season_id, team=team_id)

    normalized = []
    game_week = 0

    for game in games:
        if game.week != game_week+1:
            normalized.append(None)

        normalized.append(game)

        game_week = game.week

    return normalized
        
