import os

from trail.libconfig import libconfig
from trail.userconfig.config import MainConfig
from trail.userconfig.exceptions import MissingConfigurationException

primary_config_path = os.path.expanduser(libconfig.PRIMARY_USER_CONFIG_PATH)
secondary_config_path = os.path.expanduser(libconfig.SECONDARY_USER_CONFIG_PATH)

if os.getenv('TRAIL_CONFIG'):
    config_path = os.getenv('TRAIL_CONFIG')
elif os.path.isfile(primary_config_path):
    config_path = primary_config_path
elif os.path.isfile(secondary_config_path):
    config_path = secondary_config_path
else:
    raise MissingConfigurationException()

userconfig = MainConfig(config_path)
