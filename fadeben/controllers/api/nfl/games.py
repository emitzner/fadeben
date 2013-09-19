import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben import api

log = logging.getLogger(__name__)

class GamesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('game', 'games', controller='api/nfl/games', 
    #         path_prefix='/api/nfl', name_prefix='api_nfl_')

    def index(self, format='html'):
        """GET /api/nfl/games: All items in the collection"""
        # url('api_nfl_games')

    def show(self, id, format='html'):
        """GET /api/nfl/games/id: Show a specific item"""
        # url('api_nfl_game', id=ID)
        game = api.nfl.game.find(game_id=id)

        # TODO: give some more depth to home / away team structures
        g = {
            'game_id': game.id,
            'season': game.season_num,
            'week': game.week,
            'home_team_id': game.home_team_id,
            'away_team_id': game.away_team_id,
            'spread': game.spread,
            'home_score': game.home_score,
            'away_score': game.away_score
            }

        return self._render_json('ok', g)
