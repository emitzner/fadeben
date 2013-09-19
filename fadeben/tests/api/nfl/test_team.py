import datetime
from mock import Mock

from fadeben.tests import *

from fadeben.model import *
from fadeben import api

class TestNFLTeamAPI(TestController):
    
    def test_find_throws_exception_if_neither_team_id_or_team_abbr_is_provided(self):
        self.assertRaises(KeyError, api.nfl.team.find, banana='nope')
