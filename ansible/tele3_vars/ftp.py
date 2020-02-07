from .base import SQLVars


class FTP(SQLVars):

    def accounts(self, host):
        server = host.split('.', 1)[0]
        return self.annotated_query(('username', 'password', 'homedir', 'readonly', 'quota'), f'''
            SELECT
                login,
                hash,
                homedir,
                readonly,
                quota * 1024 * 1024
            FROM ftphosting
            WHERE server = "{server}"
            ORDER BY login
        ''')

    def values(self, host):
        return {
            'accounts': self.accounts(host),
        }
