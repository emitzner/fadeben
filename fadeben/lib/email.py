import atexit

from turbomail.control import interface
from turbomail import Message

FROM_NAME = 'FadeBen'
FROM_EMAIL = 'noreply@fadeben.com'

class TurboMailer(object):
    """
    TurboMail-specific details here:
        http://www.python-turbomail.org/docs/chapters/detailed.html
        http://packages.python.org/TurboMail/
        
        Thanks @shazow
    """
    def __init__(self, config=None):
        self.config = {
            'mail.on': True,
            'mail.transport': 'smtp',
            'mail.smtp.server': 'localhost',
            'mail.message.encoding': 'UTF-8',
            'mail.smtp.tls': True,
            'mail.smtp.debug': True,
        }
        self.config.update(config)

        def shutdown():
            interface.stop()
        atexit.register(shutdown)

        interface.start(self.config)

    def message(self, email, subject, plain, rich=None):
        m = Message(
                author=(FROM_NAME, FROM_EMAIL),
                to=email,
                subject=subject)
        m.plain = unicode(plain)
        if rich:
            m.rich = rich
        m.send()
        
class DebugMailer(object):
    mails = {}
    def __init__(self, config=None):
        pass
        
    def message(self, email, subject, plain, rich=None):
        if email not in self.mails:
            self.mails[email] = []
            
        self.mails[email].append({'subject': subject, 'plain': plain, 'rich': rich})
        
    def reset(self):
        DebugMailer.mails = {}
