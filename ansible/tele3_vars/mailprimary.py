from .base import SQLVars


class MailPrimary(SQLVars):

    GROUP = 'mail'

    def values(self, host):
        return  {
            'relayfromhosts': self.single('servers', 'fqdn'),
            'accounts': self.mapping('mailaccounts', 'login', 'hash'),
        }
