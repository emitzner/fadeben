import datetime
from mock import Mock

from fadeben.tests import *

from fadeben.model import *
from fadeben import api

from sqlalchemy.orm import exc

class TestNFLSeasonAPI(TestController):
    
    def test_weeks_completed_returns_none_when_no_games_have_been_played(self):
        game = Game()
        game.season_num = 1
        game.home_team_id = 1
        game.away_team_id = 2
        game.week = 1
        game.game_time = datetime.datetime.utcnow()
        Session.add(game)
        Session.commit()

        wc = api.nfl.season.weeks_completed(season=1)

        assert wc == 0

    def test_weeks_completed_returns_season_max_when_all_games_have_been_played(self):
        season = Season()
        season.number = 1
        season.start = datetime.datetime.utcnow()
        season.end = datetime.datetime.utcnow()
        season.num_weeks = 1
        season.num_post_weeks = 0
        

        game = Game()
        game.season_num = 1
        game.home_team_id = 1
        game.away_team_id = 2
        game.week = 1
        game.game_time = datetime.datetime.utcnow()
        game.home_score = 1
        game.away_score = 1
        game.spread = 0
        Session.add(season)
        Session.add(game)
        Session.commit()

        wc = api.nfl.season.weeks_completed(season=1)

        assert wc == 1

    def test_weeks_completed_throws_exception_when_season_doesnt_exist(self):
        self.assertRaises(exc.NoResultFound, api.nfl.season.weeks_completed, season=1)

    def test_current_week_returns_lowest_unplayed_week(self):
        game = Game()
        game.season_num = 1
        game.home_team_id = 1
        game.away_team_id = 2
        game.week = 1
        game.game_time = datetime.datetime.utcnow()
        Session.add(game)
        Session.commit()

        cw = api.nfl.season.current_week(season=1)

        assert cw == 1

    def test_current_week_throws_exception_if_season_is_over(self):
        season = Season()
        season.number = 1
        season.start = datetime.datetime.utcnow()
        season.end = datetime.datetime.utcnow()
        season.num_weeks = 1
        season.num_post_weeks = 0        

        game = Game()
        game.season_num = 1
        game.home_team_id = 1
        game.away_team_id = 2
        game.week = 1
        game.game_time = datetime.datetime.utcnow()
        game.home_score = 1
        game.away_score = 1
        game.spread = 0
        Session.add(season)
        Session.add(game)
        Session.commit()

        self.assertRaises(ValueError, api.nfl.season.current_week, season=1)
