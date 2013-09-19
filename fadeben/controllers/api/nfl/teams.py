import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben import api

log = logging.getLogger(__name__)

class TeamsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('team', 'teams', controller='api/nfl/teams', 
    #         path_prefix='/api/nfl', name_prefix='api_nfl_')

    def index(self, format='html'):
        """GET /api/nfl/teams: All items in the collection"""
        # url('api_nfl_teams')
        teams = api.nfl.team.list()

        r = []
        for team in teams:
            t = {}
            t['team_id'] = team.id
            t['name'] = team.name
            t['abbr'] = team.abbr
            r.append(t)

        return self._render_json('ok', r)

    def show(self, id, format='html'):
        """GET /api/nfl/teams/id: Show a specific item"""
        # url('api_nfl_team', id=ID)

        team = api.nfl.team.find(team_abbr=id)

        t = {
            'team_id': team.id,
            'name': team.name,
            'abbr': team.abbr,
            }

        return self._render_json('ok', t)
