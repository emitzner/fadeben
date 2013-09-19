import datetime

from fadeben.tests import *

from fadeben.model import *
from fadeben.lib.util import generate_password

# TODO: Possibly use the API in here.
class TestGameController(TestController):

    def _load(self):
        self._create_user()
        self._create_season()
        self._create_teams()
        self._create_game_without_scores()

    def test_save_many_updates_game(self):
        self._load()
        self._do_login()
        p = {
            'games': 1,
            'game-1-home-score': 1,
            'game-1-away-score': 2,
            'game-1-spread': 1,
            }

        r = self.app.post(url('save_games'), params=p)

        # make sure the game was updated
        game = Session.query(Game).get(1)

        assert game.home_score == 1
        assert game.away_score == 2
        assert game.spread == 1


    def test_leaving_info_blank_keeps_game_info_null(self):
        self._load()
        self._do_login()
        p = {
            'games': 1,
            'game-1-home-score': '',
            'game-1-away-score': '',
            'game-1-spread': '',
            }

        r = self.app.post(url('save_games'), params=p)

        # make sure the game was updated
        game = Session.query(Game).get(1)

        assert game.home_score is None
        assert game.away_score is None
        assert game.spread is None


    def test_save_multiple_games(self):
        self._load()
        self._create_game_without_scores()
        self._do_login()
        #TODO: Make a better name for this
        p = {
            'games': [1,2],
            'game-1-home-score': 1,
            'game-1-away-score': 2,
            'game-1-spread': 1,
            'game-2-home-score': 10,
            'game-2-away-score': 20,
            'game-2-spread': 10,
            }

        r = self.app.post(url('save_games'), params=p)

        # make sure the game was updated
        game = Session.query(Game).get(1)
        game2 = Session.query(Game).get(2)

        assert game.home_score == 1
        assert game.away_score == 2
        assert game.spread == 1
