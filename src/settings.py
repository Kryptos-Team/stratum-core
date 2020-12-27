from envyaml import EnvYAML
import os

# Setup BASE_DIR
from exceptions import SettingsError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Find config.yml
CONFIG_YAML = os.path.abspath(os.path.join(BASE_DIR, "config.yml"))

# Read file config.yml and parse configuration
env = EnvYAML(CONFIG_YAML)


def setup():
    """This will load config.yml and move its variables into current module"""

    def read_values(config):
        for item in config.items():
            yield item

    if os.path.exists(CONFIG_YAML):
        import sys
        module = sys.modules[__name__]
        changes = {}

        for key, value in read_values(env["server"]):
            if value != module.__dict__.get(key, None):
                changes[key] = value
            module.__dict__[key] = value
        if module.__dict__["debug"] and changes:
            print("------------")
            print("Settings:")
            for key, value in changes.items():
                print(key, ":", value)
    else:
        raise SettingsError("config.yml is missing")


setup()
