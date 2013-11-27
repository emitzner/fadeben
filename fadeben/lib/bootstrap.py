# If this file gets imported, it's going to run code.
# Use it for good.

import sys
import os
import logging

from paste.deploy import appconfig, loadapp
from logging import config
from fadeben.config.environment import load_environment
from routes.util import URLGenerator
from webtest import TestApp
from beaker.session import SessionObject

def bootstrap():
    config_file = "{0}.ini".format(os.environ.get('FB_CONFIG', 'development'))

    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(proj_dir, config_file)

    if not os.path.isfile(config_path):
        raise RuntimeError("Config file {0} does not exist in project directory".format(config_file))

    # Setup logging
    logging.config.fileConfig( os.path.join(proj_dir, config_file) )

    environ = {'HTTP_HOST': 'fadeben.btoconnor.net'}
    wsgiapp = loadapp('config:' + config_file, relative_to=proj_dir)
    config = load_environment(wsgiapp.config['global_conf'], wsgiapp.config['app_conf'])
    app = TestApp(wsgiapp, environ)
    resp = app.get('/')

    # Setup StackedProxyObjects
    import pylons
    pylons.url._push_object(URLGenerator(config['routes.map'], {'HTTP_HOST': config['fadeben.host_name']} or environ))
    pylons.app_globals._push_object(config['pylons.app_globals'])
    pylons.tmpl_context._push_object(pylons.util.ContextObj())
    pylons.translator._push_object(pylons.i18n.translation._get_translator(pylons.config.get('lang')))
    pylons.session._push_object(SessionObject(environ))
    pylons.request._push_object(resp.request)
    pylons.response._push_object(resp)
    pylons.config.update(config)

    return app

bootstrap()    
