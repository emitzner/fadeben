import logging
import formencode
import datetime
import urllib

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben.lib.schemas import GameSchema, UpdateGameSchema

from fadeben.lib import helpers as h

from fadeben import api
from fadeben.model import Session, Game

log = logging.getLogger(__name__)

class GameController(BaseController):

    def new(self):
        """Return a form for a new game"""
        c.teams = api.nfl.team.list()
        c.seasons = api.nfl.season.list()

        return render('/nfl/game/new.mako')

    def create(self):
        """Save the form post"""
        # filter shit here.

        schema = GameSchema()

        try:
            result = schema.to_python(request.params, c)
        except formencode.Invalid as e:
            log.info("bad form: {0}".format(e))
            return

        result['game_time'] = datetime.datetime(2012, 11, 10, 9, 8, 7)
        api.nfl.game.save(**result)

        log.info("all good yo, game created")

        # TODO: store flash
        
        return redirect(url('games'))

    def edit(self, id):
        c.seasons = api.nfl.season.list()
        c.teams = api.nfl.team.list()
        c.game = api.nfl.game.find(game_id=id)
        return render('/nfl/game/edit.mako')

    def edit_for_week(self, season, week):
        c.season = api.nfl.season.find(season=season)
        c.games = api.nfl.game.list(
            season=season,
            week=week
            )

        return render('/nfl/game/edit_week.mako')        

    def save(self, id):
        
        schema = GameSchema()

        try:
            result = schema.to_python(request.params, c)
        except formencode.Invalid as e:
            log.info("bad form: {0}".format(e))
            return

        result['game_id'] = id
        result['game_time'] = datetime.datetime(2012, 11, 10, 9, 8, 7)
        c.game = api.nfl.game.save(**result)

        log.info("all good yo, game edited")

        # TODO: store flash
        
        return redirect(url('games'))

    def save_many(self):
        # It's worth noting, this is a traditional end
        # point, and any ajax routes won't be handled here.

        game_ids = request.params.getall('games')

        game_ids = [int(x) for x in game_ids]

        for game_id in game_ids:
            game = Session.query(Game).get(game_id)

            schema = UpdateGameSchema()

            game_params = {
                'home_score': request.params.get('game-{0}-home-score'.format(game.id)),
                'away_score': request.params.get('game-{0}-away-score'.format(game.id)),
                'spread': request.params.get('game-{0}-spread'.format(game.id)),
                'game_time': request.params.get('game-{0}-gametime'.format(game.id)),
                }
            
            game_params = schema.to_python(game_params, c)

            # Update the game now.
            game_params['game_id'] = game_id

            game = api.nfl.game.update(**game_params)

        h.flash("Games have been successfully saved", 'success')

        if 'next' in request.GET:
            next = urllib.unquote_plus(request.GET.get('next'))
        else:
            next = url('homepage')

        return redirect(next)
