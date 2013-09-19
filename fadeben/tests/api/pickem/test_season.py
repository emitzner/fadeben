import datetime

from fadeben.tests import TestCase

from fadeben.model import Session, Season

class TestSeasonApi(TestCase):

    def test_zomg1(self):
        s = Season()
        s.number = 1
        s.num_weeks = 17
        s.num_post_weeks = 4
        s.start = datetime.datetime.now()
        s.end = datetime.datetime.now()
        Session.add(s)
        Session.commit()
        pass

    def test_zomg2(self):
        pass
