import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render

from fadeben import api

log = logging.getLogger(__name__)

class ScheduleController(BaseController):

    def season(self, season):
        # at first, render all the weeks or
        # something like that.
        # later on, we'll show the schedule for the current
        # week, with a drop down that will ajaxily load in
        # a new selected week or something like that
        c.season = api.nfl.season.find(season=season)

        return render('/nfl/schedule/season.mako')

    def week(self, season, week):
        c.season = api.nfl.season.find(season=season)

        c.games = api.nfl.game.list(season=season,
                                    week=week)

        c.week_completed = True
        for game in c.games:
            if not game.finished():
                c.week_completed = False
                break
        
        c.week = week

        return render('/nfl/schedule/week.mako')
