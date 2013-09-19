import logging
import simplejson

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from fadeben.lib.base import BaseController, render
from fadeben.lib.schemas import PredictionSchema
from fadeben import api

log = logging.getLogger(__name__)

class PredictionsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('prediction', 'predictions', controller='api/pickem/predictions', 
    #         path_prefix='/api/pickem', name_prefix='api_pickem_')
    #
    # NOTE: All 'id's in this controller reference a NFL GAME ID.

    def index(self, format='html'):
        """GET /api/pickem/predictions: All items in the collection"""
        # url('api_pickem_predictions')

    def update(self, id):
        """PUT /api/pickem/predictions/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('api_pickem_prediction', id=ID),
        #           method='put')
        # url('api_pickem_prediction', id=ID)
        # Step 1: grab params
        values = simplejson.loads(request.params['model'])
        schema = PredictionSchema()
        values = schema.to_python(values, c) # todo - catch error
        prediction = values['prediction']

        log.debug("setting prediction for {0} to {1}".format(id, prediction))

        # Step 2: Update prediction
        api.pickem.prediction.save(user_id=c.user.id, game_id=id, prediction=prediction)

        return self._render_json('ok', {})


    def show(self, id, format='html'):
        """GET /api/pickem/predictions/id: Show a specific item"""
        # url('api_pickem_prediction', id=ID)

        prediction = api.pickem.prediction.find(user_id=c.user.id,game_id=id)

        p = {
            'game_id': prediction.game_id,
            'user_id': prediction.user_id,
            'prediction': prediction.prediction,
            }

        return self._render_json('ok', p)
