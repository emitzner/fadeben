import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render

from fadeben import api

log = logging.getLogger(__name__)

class TeamController(BaseController):

    def index(self):
        c.teams = api.nfl.team.list()

        return render('/nfl/team/index.mako')

    def view(self, abbr):
        # TODO: Pull out of query param? or something like that
        c.current_season = api.nfl.season.find(season=g.current_season)
        c.team = api.nfl.team.find(team_abbr=abbr)

        # Get their games this season, too.
        c.games = api.nfl.game.list(
            season=c.current_season.number,
            team=c.team.id
            )

        c.record = api.nfl.team.get_record(team_id=c.team.id, games=c.games)
        c.record_ats = api.nfl.team.get_record(team_id=c.team.id, games=c.games, ats=True)

        return render('/nfl/team/view.mako')
