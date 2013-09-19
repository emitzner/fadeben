import sys
from fadeben.model import Session, User, Member
from fadeben.lib.util import create_random_string, generate_password

from fadeben.api.account import reset_password

def create_user(username, name, email):
    u = User()
    u.username = username
    u.name = name
    u.email = email
    u.salt = create_random_string(7)
    u.password = "banana"
    u.password = generate_password("banana", u.salt)
    Session.add(u)
    Session.commit()
    print "Username {0} created.".format(u.username)

    # Now reset their password
    reset_password(user_id=u.id)
    print "Password reset and sent for {0}.".format(u.username)

    # Add them to the pickem league
    m = Member()
    m.season_num = 48
    m.user_id = u.id
    Session.add(m)
    Session.commit()

    print "Added to pickem league for season 48"
