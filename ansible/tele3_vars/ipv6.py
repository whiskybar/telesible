from .base import SQLVars


class VIP6(SQLVars):

    def ip6conf(self, host):
        return self.annotated_query(('ipv6', 'mask', 'gw'), f'''
            SELECT ipv6, mask, gw FROM ipv6
            LEFT JOIN ipv6_block b ON (ipv6.full6 BETWEEN rangefrom AND rangeto)
            WHERE revers = "{host}."
        ''')

    def values(self, host):
        return  {
            'conf': self.ip6conf(host),
        }
