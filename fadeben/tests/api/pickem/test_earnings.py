import datetime
from mock import Mock

from fadeben.tests import *

from fadeben.model import *
from fadeben import api

class TestPickemEarningsAPI(TestController):

    def test_earnings_map_calculates_clear_winner(self):
        #api.pickem.earnings.calculate = Mock(return_value=[1])
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        simple_map = {1: {1: 5}, 2: {1: 4} }
        u1 = self._create_mock_user(1)
        u2 = self._create_mock_user(2)
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=1)
        api.pickem.prediction.count_user_week = Mock(return_value=simple_map)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.member.list = Mock(return_value=[u1, u2])
        earnings_map = api.pickem.earnings.calculate(season=47)

        assert earnings_map[1] == 1

    def test_earnings_map_calculates_clear_winner_multi_week(self):
        #api.pickem.earnings.calculate = Mock(return_value=[1])
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        multi_week_map = {1: {1: 5, 2: 1}, 2: {1: 4, 2: 10} }
        u1 = self._create_mock_user(1)
        u2 = self._create_mock_user(2)
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=2)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.prediction.count_user_week = Mock(return_value=multi_week_map)
        api.pickem.member.list = Mock(return_value=[u1, u2])

        earnings_map = api.pickem.earnings.calculate(season=47)

        assert earnings_map[1] == 1
        assert earnings_map[2] == 2

    def test_earnings_map_returns_array_for_tie(self):
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        tie_map = {1: {1: 5, 2: 10}, 2: {1: 4, 2: 10} }
        u = [User(id=x) for x in xrange(1, 3)]
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=2)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.prediction.count_user_week = Mock(return_value=tie_map)
        api.pickem.member.list = Mock(return_value=u)

        earnings_map = api.pickem.earnings.calculate(season=47)

        assert earnings_map[1] == 1
        assert earnings_map[2] == [1, 2]

    def test_earnings_map_looks_at_future_week_for_tie(self):
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        # user 1 should win week 2 since they beat user 2 in week 3
        tie_map = {1: {1: 5, 2: 10, 3: 4}, 2: {1: 4, 2: 10, 3: 1} }
        u = [User(id=x) for x in xrange(1, 3)]
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=3)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.prediction.count_user_week = Mock(return_value=tie_map)
        api.pickem.member.list = Mock(return_value=u)

        earnings_map = api.pickem.earnings.calculate(season=47)

        assert earnings_map[1] == 1
        assert earnings_map[2] == 1

    def test_earnings_map_looks_eliminates_users_when_fall_below(self):
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        # user 1 should win week 2 since they beat user 2 in week 3
        tie_map = {
            1: {1: 5, 2: 10, 3: 4, 4: 9},
            2: {1: 4, 2: 10, 3: 4, 4: 10},
            3: {1: 4, 2: 10, 3: 2, 4: 12}
        }
        u = [User(id=x) for x in xrange(1, 4)]
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=4)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.prediction.count_user_week = Mock(return_value=tie_map)
        api.pickem.member.list = Mock(return_value=u)

        earnings_map = api.pickem.earnings.calculate(season=47)

        assert earnings_map[1] == 1
        assert earnings_map[2] == 2
        assert earnings_map[3] == 2
        assert earnings_map[4] == 3

    def test_earnings_returns_array_when_tied(self):
        # Set up mocks (ruhroh)
        # map returns {user_id: {week: count} }
        # user's 1 & 2 should still be tied.
        tie_map = {
            1: {1: 5, 2: 10, 3: 4},
            2: {1: 4, 2: 10, 3: 4},
        }
        u = [User(id=x) for x in xrange(1, 3)]
        season = self._create_mock_season()

        api.nfl.season.weeks_completed = Mock(return_value=3)
        api.nfl.season.find = Mock(return_value=season)
        api.pickem.prediction.count_user_week = Mock(return_value=tie_map)
        api.pickem.member.list = Mock(return_value=u)

        earnings_map = api.pickem.earnings.calculate(season=47)

        print earnings_map
        assert earnings_map[3] == [1, 2]

    def _create_mock_user(self, user_id):
        u = User()
        u.id = user_id
        return u

    def _create_mock_season(self):
        s = Season()
        s.num_weeks = 17
        s.num_post_weeks = 4
        return s
