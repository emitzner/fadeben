from fadeben.tests import *

class TestScheduleController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='nfl/schedule', action='index'))
        # Test response...
