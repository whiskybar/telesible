from .base import SQLVars


class DNS(SQLVars):

    DATABASE = 'mydns'

    def zones(self, host):
        return self.single_query(f'''
            SELECT LEFT(origin, LENGTH(origin) - 1)
            FROM soa JOIN rr ON soa.id = rr.zone AND rr.type = "NS"
            WHERE data = "{host}." ORDER BY origin
        ''')

    def values(self, host):
        return {
            'zones': self.zones(host),
        }
