"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from fadeben.lib.email import TurboMailer
from fadeben.config.serverconfig import ServerConfig

from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))

        # Set up the emailer.
        self.mailer = TurboMailer({
                'mail.transport': config.get('mail.transport', 'debug'),
                'mail.smtp.server': config.get('mail.server', 'localhost'),
                'mail.smtp.username': config.get('mail.username'),
                'mail.smtp.password': config.get('mail.password'),
                'mail.utf8qp.on': True,
                'mail.smtp.tls': True,
            })

        self.current_season = int(config.get('fadeben.current_season'))

        self.serverconfig = ServerConfig()
