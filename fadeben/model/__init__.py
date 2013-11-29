"""The application's model objects"""
import logging
import pytz

from fadeben.model.meta import Session, Base
from fadeben.lib import dt

from sqlalchemy import Column, Integer, Unicode, Date, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship

log = logging.getLogger(__name__)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

# TODO: adjust columns appropriately, like not nullable, indexed, etc.
#       also, figure out default orderings
#       add __repr__ / __str__ for all these
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode, nullable=False, unique=True)
    name = Column(Unicode, nullable=False)
    password = Column(Unicode, nullable=False)
    salt = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False, unique=True)
    
    @property
    def first_name(self):
        return self.name.split(" ")[0]

    def __repr__(self):
        return "User<{0}>".format(self.username)

class Season(Base):
    __tablename__ = 'nfl_seasons'

    number = Column(Integer, primary_key=True)
    start = Column(Date, nullable=False, index=True)
    end = Column(Date, nullable=False)
    num_weeks = Column(Integer, nullable=False)
    num_post_weeks = Column(Integer, nullable=False)

    @property
    def num_total_weeks(self):
        return self.num_weeks + self.num_post_weeks

class Team(Base):
    __tablename__ = 'nfl_teams'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(200), unique=True)
    abbr = Column(Unicode(10), unique=True, nullable=False)
    conference = Column(Integer, nullable=False)
    division = Column(Integer, nullable=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Team<{0}>".format(self.abbr)

class Game(Base):
    __tablename__ = 'nfl_games'

    id = Column(Integer, primary_key=True)
    season_num = Column(Integer, ForeignKey('nfl_seasons.number'), index=True, nullable=False)
    week = Column(Integer, nullable=False)
    game_time = Column(DateTime, index=True, nullable=False)
    home_team_id = Column(Integer, ForeignKey('nfl_teams.id'), index=True, nullable=False)
    away_team_id = Column(Integer, ForeignKey('nfl_teams.id'), index=True, nullable=False)
    home_score = Column(Integer)
    away_score = Column(Integer)
    spread = Column(Integer)

    # relations
    home_team = relationship(Team, primaryjoin=home_team_id == Team.id)
    away_team = relationship(Team, primaryjoin=away_team_id == Team.id)

    def is_finished(self):
        return (not (self.home_score is None))
        
    def finished(self):
        """This is deprecated.  Please use is_finished()"""
        return self.is_finished()

    def short_display(self):
        return "{0} @ {1}".format(self.away_team.abbr, self.home_team.abbr)

    @property
    def game_time_l(self):
        """Game time, converted from UTC to America/New_York"""
        # TODO: put timezone in the config.
        return dt.localfromutc(self.game_time, pytz.timezone('America/New_York'))

    def __str__(self):
        return "Game<{0}>".format(self.id)

    def __repr__(self):
        return "Game<{0}>".format(self.id)

    def winner(self, ats=False):
        if self.home_score is None:
            raise ValueError
        h_s = self.home_score
        a_s = self.away_score

        if ats:
            h_s += self.spread

        if h_s > self.away_score:
            return self.home_team_id
        elif self.away_score > h_s:
            return self.away_team_id
        else:
            return None

class Prediction(Base):
    __tablename__ = 'pickem_predictions'
    __table_args__ = ( UniqueConstraint('user_id', 'game_id'), )

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    game_id = Column(Integer, ForeignKey('nfl_games.id'), primary_key=True, nullable=False)
    prediction = Column(Boolean, nullable=False)

    # relations
    user = relationship(User, primaryjoin=user_id == User.id)
    game = relationship(Game, primaryjoin=game_id == Game.id)

    def __str__(self):
        return "< {0}, {1}: {2} >".format(self.user_id, self.game_id, self.prediction)

    def __repr__(self):
        return "Prediction<{0}, {1}: {2}>".format(
            self.user_id, self.game_id, self.prediction)
    

class Member(Base):
    __tablename__ = 'pickem_membership'
    
    season_num = Column(Integer, ForeignKey('nfl_seasons.number'), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)

    season = relationship(Season, primaryjoin=season_num==Season.number)
    user = relationship(User, primaryjoin=user_id==User.id)
