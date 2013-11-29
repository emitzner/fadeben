import logging

from pylons import tmpl_context as c, app_globals as g
from pylons.templating import render_mako as render

from unstdlib.standard import get_many

from fadeben.model import Session, Member, User

log = logging.getLogger(__name__)

def list(**params):
    """
    :param season
    """

    season = params['season']

    q = Session.query(User)
    q = q.join(Member)

    q = q.filter(Member.season_num==season)

    q = q.order_by(User.name)

    return q.all()

def send_reminder(**params):
    user_id, games = get_many(params, ['user_id', 'games'])

    if not games:
        raise ValueError

    c.user = Session.query(User).get(user_id)
    c.season = games[0].season_num
    c.week = games[0].week #zomg hack
    c.games = games

    subject = "Reminder: You've got {0} games to predict today".format(
        len(games)
        )

    content = render('/email/reminder.mako')

    g.mailer.message(c.user.email, subject, content)
