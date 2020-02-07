from .base import SQLVars


class DNSMaster(SQLVars):

    DATABASE = 'mydns'

    def slaves(self, host):
        return self.single_query(f'''
            SELECT l.ipv4 FROM bind__signers s
            LEFT JOIN bind__signer_group g ON (g.signerid = s.id)
            LEFT JOIN bind__slaves l ON (l.grpid = g.groupid)
            WHERE s.`name` = "{host}" AND l.ipv4 IS NOT NULL
            GROUP BY l.ipv4
            UNION
            SELECT l.ipv6 FROM bind__signers s
            LEFT JOIN bind__signer_group g ON (g.signerid = s.id)
            LEFT JOIN bind__slaves l ON (l.grpid = g.groupid)
            WHERE s.`name` = "{host}" AND l.ipv6 IS NOT NULL
            GROUP BY l.ipv6
        ''')

    def values(self, host):
        return  {
            'slave': self.slaves(host),
        }
