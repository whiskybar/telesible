from collections import defaultdict
import mysql.connector

from ansible.plugins.inventory import BaseInventoryPlugin


DOCUMENTATION = '''
  name: tele3
  plugin_type: inventory
  short_description: TELE3 servers
  requirements:
    - mysql-connector-python
  description:
    - create inventory from MySQL tables on ghostdog
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
        - database which contains the configuration
      ini:
        - section: tele3
          key: database
      env:
        - name: ANSIBLE_TELE3_DATABASE
      default: hosting
'''


SERVER_SQL='''
    SELECT housing.fqdn, server_roles.role, housing_destinations.location
    FROM housing
        LEFT JOIN server_roles ON server_roles.id = housing.id
        LEFT JOIN ip_addresses ON ip_addresses.id = housing.ip
        LEFT JOIN housing_destinations ON housing_destinations.id = ip_addresses.destination
    WHERE housing.fqdn IS NOT NULL AND server_roles.role IS NOT NULL
'''

class InventoryModule(BaseInventoryPlugin):

    _load_name = NAME = 'tele3'  # not sure why if fails without _load_name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = mysql.connector.connect(
            option_files=self.get_option('option_file'),
            database=self.get_option('database'),
        )
        self.cursor = self.connection.cursor()

    def verify_file(self, path):
        return True  # unclear why this is needed

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path, cache)
        self.inventory.add_host('localhost')

        self.cursor.execute(SERVER_SQL)

        roles = defaultdict(list)
        for hostname, role, location in self.cursor:
            if role:
                role = role.replace('-', '_').replace(' ', '_')
                self.inventory.add_group(role)
                self.inventory.add_host(hostname, role)
                roles[hostname].append(role)

            if location:
                location = location.replace('-', '_').replace(' ', '_')
                self.inventory.add_group(location)
                self.inventory.add_host(hostname, location)
                self.inventory.set_variable(hostname, 'location', location)

        for hostname, roles in roles.items():
            self.inventory.set_variable(hostname, 'roles', roles)
