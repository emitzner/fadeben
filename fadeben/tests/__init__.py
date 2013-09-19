"""Pylons application test package

This package assumes the Pylons environment is already loaded, such as
when this script is imported from the `nosetests --with-pylons=test.ini`
command.

This module initializes the application via ``websetup`` (`paster
setup-app`) and provides the base testing objects.
"""
from unittest import TestCase
import os
import sys
import datetime

import pylons
from pylons.i18n.translation import _get_translator
from paste.deploy import loadapp
from pylons import url
from paste.script.appinstall import SetupCommand
from routes.util import URLGenerator
from webtest import TestApp

from fadeben.config.environment import load_environment

from fadeben import model
Session = model.Session

__all__ = ['environ', 'url', 'TestController']

environ = {}
here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(os.path.dirname(here_dir))

sys.path.insert(0, conf_dir)

class TestModel(TestCase):

    def setUp(self):
        model.Base.metadata.create_all(bind=Session.bind)

    def tearDown(self):
        Session.rollback()
        model.Base.metadata.drop_all(bind=Session.bind)


from fadeben.lib.util import generate_password

class TestController(TestModel):
    def __init__(self, *args, **kwargs):
        wsgiapp = loadapp('config:test.ini', relative_to=conf_dir)
        config = wsgiapp.config
        pylons.app_globals._push_object(config['pylons.app_globals'])
        pylons.config._push_object(config)
        
        # Initialize a translator for tests that utilize i18n
        translator = _get_translator(pylons.config.get('lang'))
        pylons.translator._push_object(translator)
        
        url._push_object(URLGenerator(config['routes.map'], environ))
        self.app = TestApp(wsgiapp)
        TestCase.__init__(self, *args, **kwargs)

    
    def _create_season(self):
        s = model.Season()
        s.number = 45
        s.start = datetime.date(2011, 10, 5)
        s.end = datetime.date(2013, 4, 4)

        s.num_weeks = 17
        s.num_post_weeks = 4

        Session.add(s)
        Session.commit()
        return s

    def _create_teams(self):
        t = model.Team()
        t.name = u"team 1"
        t.abbr = u"t1"
        t.conference = 1
        t.division = 1
        t2 = model.Team()
        t2.name = u"team 1"
        t2.abbr = u"t1"
        t2.conference = 1
        t2.division = 1
        Session.add(t2)
        Session.commit()

    def _create_game_without_scores(self):
        g = model.Game()
        g.home_team_id = 1
        g.away_team_id = 2
        g.game_time = datetime.datetime(2012, 05, 05, 05, 05, 05)
        g.season_num = 47
        g.week = 1
        Session.add(g)
        Session.commit()

    def _create_user(self):
        u = model.User()
        u.username = u"test"
        u.name = u"Test User"
        u.email = u"test@test.com"
        u.salt = u"banana"
        u.password = generate_password('zomg', u.salt)
        Session.add(u)
        Session.commit()

    def _do_login(self):
        p = {'username': u'test', 'password': u'zomg'}
        r = self.app.post(url('login'), params=p).follow()
