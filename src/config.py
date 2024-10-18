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
    post_metadata = {}

    # Parse post metadata.
    post_header_metadata = configparser.ConfigParser()
    post_header_metadata.read_string(post_header_string)
    if post_header_metadata.has_section("metadata"):
        for k, v in post_header_metadata.items("metadata"):
            post_metadata[k] = v

    # Insert global metadata (higher precedence).
    if _global_config.has_section("metadata"):
        for k, v in _global_config.items("metadata"):
            post_metadata[k] = v

    return post_metadata
