from fadeben.tests import *

class TestPredictionController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pickem/prediction', action='index'))
        # Test response...
