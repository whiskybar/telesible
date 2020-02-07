from .base import SQLVars


class Web(SQLVars):

    def domains(self, host):
        server = host.split('.', 1)[0]
        return self.annotated_query(('domain', 'aliases', 'homedir', 'php_version', 'LE', 'http2'), f'''
            SELECT
                domain,
                REPLACE(IFNULL(server_aliases, CONCAT('www.', domain)), '\n', ' '),
                homedir,
                php_version,
                LE,
                http2
            FROM domains
            WHERE server = "{server}"
        ''')

    def ftp(self, host):
        server = host.split('.', 1)[0]
        return self.annotated_query(('username', 'password', 'readonly', 'homedir', 'quota'), f'''
            SELECT
                userid,
                hash,
                FALSE,
                homedir,
                quota * 1024 * 1024
            FROM domains
            WHERE server = "{server}" AND homedir != "" AND homedir IS NOT NULL AND userid != "" AND userid IS NOT NULL
        ''')

    def values(self, host):
        return {
            'domains': self.domains(host),
            'ftp': self.ftp(host),
        }
