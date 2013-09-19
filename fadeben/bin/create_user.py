import sys
from fadeben.model import Session, User
from fadeben.lib.util import create_random_string, generate_password

def create_user(username, name, password, email):
    u = User()
    u.username = username
    u.name = name
    u.email = email
    u.salt = create_random_string(7)
    u.password = generate_password(password, u.salt)
    Session.add(u)
    Session.commit()
    print "Username {0} created.".format(u.username)
