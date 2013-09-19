import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render

log = logging.getLogger(__name__)

class WelcomeController(BaseController):

    def homepage(self):
        # Until I find something to do with this page, just redirect
        # to the standings page.
        # get the current season
        current_season = g.current_season
        return redirect(url("standings", season=current_season))
        return render('/welcome/homepage.mako')
