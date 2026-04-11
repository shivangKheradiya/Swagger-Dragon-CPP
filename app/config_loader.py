import os
import tomllib


# ---------------------------------------------------------
# Location of config file
# ---------------------------------------------------------
CONFIG_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "defaults",
    "config.toml"
)


_cached_config = None
_cached_mtime = 0


def get_config(force_reload: bool = False) -> dict:
    """
    Load and cache config.toml.

    - Reloads automatically if file is modified
    - Returns config as a dictionary
    """
    global _cached_config, _cached_mtime

    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

    mtime = os.path.getmtime(CONFIG_FILE)

    if force_reload or _cached_config is None or mtime != _cached_mtime:
        with open(CONFIG_FILE, "rb") as f:
            _cached_config = tomllib.load(f)
        _cached_mtime = mtime

    return _cached_config