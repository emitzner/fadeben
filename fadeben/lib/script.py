import logging
import os
from paste.deploy import appconfig, loadapp
from logging import config
from fadeben.config.environment import load_environment

def bootstrap(config_file, path):
    from routes.util import URLGenerator
    from webtest import TestApp
    from beaker.session import SessionObject

    # Setup logging
    logging.config.fileConfig( os.path.join(path, config_file) )

    environ = {'HTTP_HOST': 'fadeben.btoconnor.net'}
    wsgiapp = loadapp('config:' + config_file, relative_to=path)
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

