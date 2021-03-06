from fadeben.tests import *

class TestGamesController(TestController):

    def test_index(self):
        response = self.app.get(url('api_nfl_games'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_api_nfl_games', format='xml'))

    def test_create(self):
        response = self.app.post(url('api_nfl_games'))

    def test_new(self):
        response = self.app.get(url('api_nfl_new_game'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_api_nfl_new_game', format='xml'))

    def test_update(self):
        response = self.app.put(url('api_nfl_game', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('api_nfl_game', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('api_nfl_game', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('api_nfl_game', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('api_nfl_game', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_api_nfl_game', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('api_nfl_edit_game', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_api_nfl_edit_game', id=1, format='xml'))
