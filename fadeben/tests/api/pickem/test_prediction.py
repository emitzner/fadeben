import datetime

from fadeben.tests import *

from fadeben.model import *
from fadeben import api

from fadeben.lib.util import generate_password

class TestPickemAPI(TestController):

    def _load(self):
        self._create_user()
        self._create_season()
        self._create_teams()
        self._create_game_without_scores()

    def test_find_missing_returns_game(self):
        self._load()

        start_date = datetime.datetime(2010, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2013, 1, 1, 0, 0, 0)

        unpredicted_games = api.pickem.prediction.find_unpredicted(
            user_id=1, start_date=start_date, end_date=end_date)

        assert len(unpredicted_games) == 1
        assert unpredicted_games[0].id == 1
        # No predictions should be made

    def test_find_missing_doesnt_return_game_that_has_prediction(self):
        self._load()

        p = Prediction()
        p.user_id = 1
        p.game_id = 1
        p.prediction = True
        Session.add(p)
        Session.commit()

        start_date = datetime.datetime(2010, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2013, 1, 1, 0, 0, 0)

        unpredicted_games = api.pickem.prediction.find_unpredicted(
            user_id=1, start_date=start_date, end_date=end_date)

        assert len(unpredicted_games) == 0

    def test_find_missing_doesnt_count_other_users_predictions(self):
        self._load()

        p = Prediction()
        p.user_id = 2
        p.game_id = 1
        p.prediction = True
        Session.add(p)
        Session.commit()

        start_date = datetime.datetime(2010, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2013, 1, 1, 0, 0, 0)

        unpredicted_games = api.pickem.prediction.find_unpredicted(
            user_id=1, start_date=start_date, end_date=end_date)

        assert len(unpredicted_games) == 1

    def test_find_missing_doesnt_count_games_outside_of_range(self):
        self._load()

        start_date = datetime.datetime(2013, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2014, 1, 1, 0, 0, 0)

        unpredicted_games = api.pickem.prediction.find_unpredicted(
            user_id=1, start_date=start_date, end_date=end_date)

        assert len(unpredicted_games) == 0
