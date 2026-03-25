import tomllib, os

CONFIG_FILE = os.path.abspath("defaults") + "/config.toml"

_cached = None
_mtime = 0

def get_config(force=False):
    global _cached, _mtime
    mtime = os.path.getmtime(CONFIG_FILE)

    if force or _cached is None or mtime != _mtime:
        with open(CONFIG_FILE, "rb") as f:
            _cached = tomllib.load(f)
        _mtime = mtime

    return _cached