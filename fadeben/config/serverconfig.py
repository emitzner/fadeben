import logging

from pylons import config
from pylons.controllers.util import redirect, abort
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)
class ServerConfig(object):
    prefix = 'fadeben.'

    def is_enabled(self, key, user=None):
        val = config.get('{0}{1}'.format(self.prefix, key), False)
        # if val == 'admin':
        #     return (user or {}).get('admin', False)
        return asbool(val)

    def get_value(self, key):
        return config.get('{0}{1}'.format(self.prefix, key))
