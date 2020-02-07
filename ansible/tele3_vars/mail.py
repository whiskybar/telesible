from .base import SQLVars


class Mail(SQLVars):

    def trash(self):
        return self.mapping_query('SELECT domain, domaintrash FROM domains WHERE domaintrash != ""')

    def values(self, host):
        return  {
            'recipients': self.single('mailrecipients', 'recipient'),
            'nospamhosts': self.single('nospamhosts', 'host'),
            'nospamrecipients': self.single('nospamrecipients', 'recipient'),
            'spam': self.single('spam', 'text'),
            'aliases': self.mapping('mailaliases', 'source', 'destination'),
            'redirects': self.mapping('mailredirects', 'source', 'destination'),
            'trash': self.trash(),
        }
