import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben import api

log = logging.getLogger(__name__)

class SeasonController(BaseController):

    def index(self):
        """Returns a list of Seasons"""
        c.seasons = api.nfl.season.list()
        return render('/nfl/season/index.mako')

    def view(self, number):
        c.season = api.nfl.season.find(season=number)
        c.current_week = api.nfl.season.current_week(season=number)

        return render('/nfl/season/view.mako')
