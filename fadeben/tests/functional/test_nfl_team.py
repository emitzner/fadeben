from fadeben.tests import *

class TestTeamController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nfl/team', action='index'))
        # Test response...
