from fadeben.tests import *

class TestStandingsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pickem/standings', action='index'))
        # Test response...
