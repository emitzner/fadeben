import logging
import formencode
import formencode.htmlfill
import urllib

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from fadeben.lib import helpers as h

from fadeben.lib.base import BaseController, render
from fadeben.lib.schemas import LoginSchema, ChangePasswordSchema, ResetPasswordSchema
from fadeben.lib.util import generate_password, create_random_string

from fadeben import api

from fadeben.model import Session, User

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def login(self):
        if request.method == 'GET':
            self._handle_login_get()
        else:
            self._handle_login_post()

        return render('/account/login.mako')

    def settings(self):
        return render('/account/settings.mako')

    def change_password(self):
        return render('/account/change_password.mako')

    def change_password_submit(self):
        schema = ChangePasswordSchema()

        try:
            form_result = schema.to_python(request.POST, c)
        except formencode.Invalid as error:
            #TODOLAUNCH: show error message.
            log.debug("there was an error with form stuff yo")
            raise #TODOLAUNCH: don't do this

        # Make sure the password they entered was the actual password
        p = generate_password(form_result['old_password'], c.user.salt)
        if c.user.password != p:
            #TODOLAUNCH: handle this like a real engineer
            raise Exception("The password you entered was not right")

        api.account.change_password(user_id=c.user.id,
                                    new_password=form_result['new_password1'])

        log.info("User {0} has changed their password.".format(c.user.id))

        h.flash("Your password has been successfully updated.")
        return redirect(url('settings'))

    def _handle_login_get(self):
        return render('/account/login.mako')

    def _handle_login_post(self):
        schema = LoginSchema()

        try:
            form_result = schema.to_python(request.POST, c)
        except formencode.Invalid as error:
            log.debug("There was an error with the form stuff yo.")
            raise

        # Find the user.
        user = Session.query(User).filter(User.username == form_result['username']).first()
        log.debug("user found? {0}".format(user))

        if user is None \
                or user.password != generate_password(form_result['password'], user.salt):
            c.form_result = form_result
            c.form_errors = {'__global__':
                                 'The username / password combination '
                             'you entered could not be found'}
            log.info("Incorrect login information.")
            return formencode.htmlfill.render(

                render('/account/login.mako'),
                defaults=c.form_result,
                errors=c.form_errors
                )

        # update session
        session['user_id'] = user.id
        session.save()

        log.info("User {0} has logged in.".format(user.username))

        if 'next' in request.GET:
            log.debug("yup")
            next = urllib.unquote_plus(request.GET.get('next'))
        else:
            next = url('homepage')
        
        return redirect(next)

    def logout(self):
        session.invalidate()
        session.save()
        return redirect(url('homepage'))

    def forgot_password(self):
        # Logged out users only
        if c.user:
            return redirect(url('homepage'))

        log.debug("oh hai")

        if request.method == 'GET':
            return self._display_forgot_password()
        else:
            return self._handle_forgot_password()

    def _display_forgot_password(self):
        return render('/account/reset_password.mako')

    def _handle_forgot_password(self):        
        schema = ResetPasswordSchema()

        try:
            form_result = schema.to_python(request.POST, c)
        except formencode.Invalid as e:
            #invalid email
            # TODOLAUNCH: handle this
            raise

        # find the user with that email
        # TODO: Error handling around this
        user = Session.query(User).filter(User.email==form_result['email']).one()

        # Reset the password
        api.account.reset_password(user_id=user.id)

        h.flash("Your password has been reset.  It will be sent in an email shortly.")
        return redirect(url("login"))
