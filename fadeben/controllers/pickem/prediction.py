import logging
import formencode
import urllib

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben.lib.schemas import PredictionSchema
from fadeben.lib import helpers as h
from fadeben import api

from fadeben.model import Session, Prediction

log = logging.getLogger(__name__)

class PredictionController(BaseController):

    def season(self, season_id):
        # just show a list of predictions for now.
        # consider redirecting at some point, but right now it's bombing

        c.season = api.nfl.season.find(season=season_id)
        try:
            c.current_week = api.nfl.season.current_week(season=season_id)
        except ValueError:
            c.current_week = None

        return render('/pickem/prediction/season.mako')

    def week(self, season_id, week):
        c.games = api.nfl.game.list(season=season_id, week=week, not_started=True)
        c.predictions = api.pickem.prediction.list(season=season_id,
                                                   week=week,
                                                   user_id=c.user.id)

        c.season = season_id
        c.week = week

        c.pmap = {}
        
        # make a map of game -> predictions for this user
        # so that we can preselect these mofos.
        for p in c.predictions:
            c.pmap[p.game_id] = p.prediction
            
        return render('/pickem/prediction/index.mako')

    def bulk(self):
        """
        This is a bulk updater for predictions.

        The main parameter is a 'game' array.  For each game id 'x' in that array, there
        should be another request param prediction-x.
        """

        if 'next' in request.GET:
            redirect_url = urllib.unquote_plus(request.GET.get('next'))
        else:
            redirect_url = url("homepage")

        # get all the games, etc etc.
        log.debug("game ids: {0}".format(request.params.getall("game")))

        game_ids = request.params.getall('game')

        # TODO this doesn't seem great
        res = [ dict(user_id=c.user.id, game_id=x, prediction=request.params.get('prediction-{0}'.format(x))) for x in game_ids]

        log.debug("res is {0}".format(res))

        schema = PredictionSchema()

        for result in res:
            if result['prediction'] is None:
                log.debug("skipping game id because its none yo {0}".format(result['game_id']))
                continue
            try:
                form_result = schema.to_python({'prediction': result['prediction']}, c)
            except formencode.Invalid as e:
                log.error("sad")
                # TODO: Handle this a bit more gracefully.
                return
            result['prediction'] = form_result['prediction']
            log.info("fr: {0}".format(result))
            try:
                api.pickem.prediction.save(**result)
            except Exception as error:
                #TODOLAUNCH: HANDLE THESE ERRORS BETTER WITH LIKE A
                # FLASH OR SOMETHING YA KNOW?
                log.error("couldn't save game {0}".format(result['game_id']))
                continue

        #TODO: This needs to reflect the number of successful predictions saved,
        # and add another flash if we couldn't save some.
        h.flash("Your predictions have been saved", 'success')
        return redirect(redirect_url)
