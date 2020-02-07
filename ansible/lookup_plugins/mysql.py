import mysql.connector
from mysql.connector import errors

DOCUMENTATION = """
  name: mysql
  plugin_type: lookup
  short_description: TELE3 domain
  requirements:
    - mysql-connector-python
  description:
    - perform any mysql command on the localhos
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
        - default database to connect to
      ini:
        - section: tele3
          key: database
      env:
        - name: ANSIBLE_TELE3_DATABASE
      default: hosting
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native, to_text


try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class LookupModule(LookupBase):

    _load_name = NAME = 'mysql'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = mysql.connector.connect(
            option_files=self.get_option('option_file'),
            database=self.get_option('database'),
        )
        self.cursor = self.connection.cursor(named_tuple=True)

    def run(self, terms, variables=None, **kwargs):
        terms = list(map(str, terms))
        self.cursor.execute(terms[0], terms[1:])
        if self.cursor.with_rows:
          return self.cursor.fetchall()
