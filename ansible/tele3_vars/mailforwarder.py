from .base import SQLVars


class MailForwarder(SQLVars):

    GROUP = 'mail'

    def values(self, host):
        return  {
            'forwarder': self.mapping('mailforwarder', 'source', 'destination'),
        }
