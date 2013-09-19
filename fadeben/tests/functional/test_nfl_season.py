from fadeben.tests import *

class TestSeasonController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nfl/season', action='index'))
        # Test response...
