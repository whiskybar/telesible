import sys
import os.path

# Patch the ansible core to allow for configuring vars plugins
import ansible
if 'vars' not in ansible.constants.CONFIGURABLE_PLUGINS:
    ansible.constants.CONFIGURABLE_PLUGINS += ('vars',)

from ansible.errors import AnsibleParserError
from ansible.plugins import AnsiblePlugin
from ansible.utils.display import Display
from ansible.inventory.host import Host
from ansible.inventory.group import Group
from ansible.utils.vars import combine_vars


DOCUMENTATION = '''
    vars: tele3
    short_description: Host variables from the TELE3 db
    description:
        - Loads variables using tele3_var plugins (providers)
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
        default_database:
          description:
            - the default database for the providers
          ini:
            - section: tele3
              key: database
          env:
            - name: ANSIBLE_TELE3_DATABASE
          default: hosting
        vars_providers:
          description:
            - directory to look for vars providers
          ini:
            - section: tele3
              key: vars_providers
          env:
            - name: ANSIBLE_TELE3_VARS_PROVIDERS
          default: None
'''


display = Display()


class VarsModule(AnsiblePlugin):

    _load_name = NAME = 'tele3'

    def __init__(self):
        super().__init__()
        self.display = display
        self.load_providers()

    def load_providers(self):
        sys.path.insert(0, os.path.dirname(self.get_option('vars_providers')))
        from tele3_vars import var_classes

        self.providers = {}
        for var_class in var_classes:
            self.providers[var_class.__name__.lower()] = var_class(
                option_file=self.get_option('option_file'),
                default_database=self.get_option('default_database'),
            )

        del sys.path[0]

    def get_vars(self, loader, path, entities, cache=True):
        result = {}
        for entity in entities:
            if not isinstance(entity, Host):
                continue

            for group in entity.get_groups():
                try:
                    provider = self.providers[group.name]
                except KeyError:
                    continue
                result = combine_vars(result, {provider.group: provider.values(entity.name)})
        return result
