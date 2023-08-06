import os

import yaml

from trail.libconfig import libconfig


class MissingConfigurationException(Exception):
    EXAMPLE_CONFIG = {
        'username': '<YOUR_USERNAME>',
        'password': '<YOUR_PASSWORD>',
        'projects': {
            'myProjectAlias': {
                'id': '1234ABC',
                'parentExperimentId': 'ABCD123'
            }
        }
    }

    def __init__(self):
        self.create_example_config()

        super().__init__(
            f"Configuration file not found. An example configuration was "
            f"automatically created at '{libconfig.SECONDARY_USER_CONFIG_PATH}'"
        )

    def create_example_config(self):
        expanded_path = os.path.expanduser(libconfig.SECONDARY_USER_CONFIG_PATH)
        with open(expanded_path, 'w') as f:
            yaml.dump(self.EXAMPLE_CONFIG, f, sort_keys=False)
