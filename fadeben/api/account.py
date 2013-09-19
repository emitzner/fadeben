from fadeben.lib.util import create_random_string, generate_password
from fadeben.model import Session, User
from pylons import app_globals as g, url

from unstdlib.standard import get_many

def list(**params):
    pass

def change_password(**params):
    required = ['user_id', 'new_password']

    user_id, new_password = get_many(params, required)

    user = Session.query(User).get(user_id)

    # make a new salt
    user.salt = create_random_string(7)
    user.password = generate_password(new_password, user.salt)

    Session.add(user)
    Session.commit()

    return user

def reset_password(**params):
    # Generate a random, new password.
    
    user_id = params['user_id']
    user = Session.query(User).get(user_id)
    random_password = create_random_string(15)

    # Change it.
    change_password(user_id=user_id, new_password=random_password)

    site_url = url("homepage", qualified=True)

    subject = "Your FadeBen password has been reset"
    content = "Your username: {0}, password is: {1}\n\n Log in here: {2}".format(user.username, random_password, site_url)

    # Email user
    g.mailer.message(user.email, subject, content)
