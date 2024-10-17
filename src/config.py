# Contains functionality related to parsing global and post metadata.


import os
import configparser


# The global config file.
_global_config = None


# Parses the config file.
def init(config_file_path):
    global _global_config
    if _global_config is None and os.path.exists(config_file_path):
        _global_config = configparser.ConfigParser()
        _global_config.read(config_file_path)
        return True
    return False


# Checks if the global config contains an option.
def has(option):
    if not _global_config is None:
        return _global_config.has_option("config", option)
    return False


# Gets a config option value the global config.
def get(option):
    if not _global_config is None:
        return _global_config.get("config", option)


# Parses metadata from post headers, combines with global metadata.
def get_post_metadata(post_header_string):
    pass
