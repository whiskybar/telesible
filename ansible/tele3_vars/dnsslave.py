from .base import SQLVars


class DNSSlave(SQLVars):

    DATABASE = 'mydns'

    def signers(self, host):
        return self.single_query(f'''
            SELECT r.ipv6 FROM bind__slaves s
            LEFT JOIN bind__signer_group g ON (g.groupid = s.grpid)
            LEFT JOIN bind__signers r ON (r.id = g.signerid)
            WHERE `slave` = "{host}" AND r.ipv6 IS NOT NULL
            UNION
            SELECT r.ipv4 FROM bind__slaves s
            LEFT JOIN bind__signer_group g ON (g.groupid = s.grpid)
            LEFT JOIN bind__signers r ON (r.id = g.signerid)
            WHERE `slave` = "{host}" AND r.ipv4 IS NOT NULL
            UNION
            SELECT allow FROM bind__allow_recursion
            WHERE `slave` = "{host}"
        ''')

    def values(self, host):
        return {
            'signer': self.signers(host),
        }
