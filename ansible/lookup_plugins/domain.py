import mysql.connector

DOCUMENTATION = """
  name: domain
  plugin_type: lookup
  short_description: TELE3 domain
  requirements:
    - mysql-connector-python
  description:
    - lookup a domain and return the entire row
  options:
    option_file:
      description:
        - MySQL connection file
        - Connect to the localhost without password if not provided
      ini:
        - section: tele3
          key: option_file
      env:
        - name: ANSIBLE_TELE3_OPTION_FILE
      default: None
    database:
      description:
        - database which contains the table domains
      ini:
        - section: tele3
          key: database
      env:
        - name: ANSIBLE_TELE3_DATABASE
      default: hosting
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


DOMAIN_COLUMNS = ('domain', 'aliases', 'php_version', 'LE', 'http2', 'username', 'password', 'readonly', 'homedir', 'quota')

DOMAIN_SQL =  '''
   SELECT
     domain,
     IFNULL(server_aliases, CONCAT('www.', domain)),
     php_version,
     LE,
     http2,
     userid,
     hash,
     FALSE,
     homedir,
     quota
   FROM domains
   WHERE domain = "%s"
'''

class LookupModule(LookupBase):

    _load_name = NAME = 'domain'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = mysql.connector.connect(
            option_files=self.get_option('option_file'),
            database=self.get_option('database'),
        )
        self.cursor = self.connection.cursor()

    def run(self, terms, variables=None, **kwargs):
        result = []
        for domain in map(str, terms):
            self.cursor.execute(DOMAIN_SQL % domain)
            rows = self.cursor.fetchall()
            if not rows:
                continue
            result.append(dict(zip(DOMAIN_COLUMNS, rows[0])))
        return result


