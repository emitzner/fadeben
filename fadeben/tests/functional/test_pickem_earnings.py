from fadeben.tests import *

class TestEarningsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pickem/earnings', action='index'))
        # Test response...
