"""The base Controller API

Provides the BaseController class for subclassing.
"""
import logging
import os
import simplejson

from pylons import tmpl_context as c, session, request, response, url, app_globals as g
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect
from pylons.templating import render_mako, cached_template, pylons_globals

from webhelpers.html import literal

from mako.lookup import TemplateLookup
from mako.exceptions import TopLevelLookupException

from fadeben.model.meta import Session
from fadeben.model import User

log = logging.getLogger(__name__)

def is_mobile(user_agent):
    enabled = ['Android', 'iPhone', 'BlackBerry']

    mobile = False
    # check the session first
    if not 'm' in session:
        for s in enabled:
            if s in user_agent:
                mobile = True
                session['m'] = True
                session.save()
                break
    else:
        mobile = session['m']

    return mobile

def render(template_name, extra_vars=None, cache_key=None,
                cache_type=None, cache_expire=None):

    if g.serverconfig.is_enabled('mobile'):
        if g.serverconfig.is_enabled('force_mobile') \
                or is_mobile(request.user_agent):
            try:
                mobile_prefix = '/mobile'
                mobile_template = '{0}{1}'.format(mobile_prefix, template_name)
                return render_mako(mobile_template, extra_vars, cache_key,
                                   cache_type, cache_expire)
            except TopLevelLookupException:
                log.debug("template not found {0}".format(mobile_template))

    return render_mako(template_name, extra_vars, cache_key,
                       cache_type, cache_expire)

class BaseController(WSGIController):

    def __before__(self):
        if 'user_id' in session:
            # find the user
            c.user = Session.query(User).filter(User.id==session['user_id']).first()
        else:
            # If they aren't at the login screen, redirect them there.
            c.user = None
            if not (request.path.startswith(url('login')) \
                    or request.path.startswith(url('reset_password'))):
                redirect(url('login', next=request.path))
        log.debug("rp: {0}".format(request.path))

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def _render_json(self, type_, response_dict):
        valid_types = {'ok': 200, 'error': 400}
            
        response.status_int = valid_types[type_]
        response.content_type = 'application/json'
        
        return simplejson.dumps(response_dict)
