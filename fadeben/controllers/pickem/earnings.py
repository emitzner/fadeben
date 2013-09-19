import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons import app_globals as g
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render

from fadeben import api

log = logging.getLogger(__name__)

class EarningsController(BaseController):

    def index(self, season_id):
        c.earnings_map = api.pickem.earnings.calculate(season=season_id)
        c.members = api.pickem.member.list(season=season_id)
        weeks_completed = api.pickem.season.weeks_completed_p(season_id=season_id)

        week_amount = int(g.serverconfig.get_value("week_amount"))
        season_amount = int(g.serverconfig.get_value("season_amount"))

        total_spent = (weeks_completed * week_amount)
        
        e = {}

        # initialize calculator
        for member in c.members:
            e[ member.id ] = 0

        for winner in c.earnings_map:
            if winner and not isinstance(winner, list):
                # tie
                e[ winner ] += (week_amount * (len(c.members)) )

        # Get overall winner.
        season_winner = api.pickem.earnings.overall_winner(season_id=season_id)

        if season_winner:
            e[ season_winner ] += (season_amount * (len(c.members)))
            total_spent += season_amount

        c.total_spent = total_spent
        log.debug("Total spent: {0}".format(c.total_spent))

        c.e = e
        return render('pickem/earnings/index.mako')
