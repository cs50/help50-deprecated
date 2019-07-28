import contextlib
import os
import re
import sys

import lib50

from . import HELPERS, PREPROCESSORS

lib50.set_local_path(os.environ.get("HELP50_PATH", "~/.local/share/help50"))
CONFIG_LOADER = lib50.config.Loader("help50")


@contextlib.contextmanager
def _syspath(newpath):
    """ Useful contextmanager that temporarily replaces sys.path. """
    oldpath = sys.path
    sys.path = newpath
    try:
        yield
    finally:
        sys.path = oldpath


def load_config(dir):
    """ Read cs50 YAML file and apply default configuration to unspecified fields.  """
    options = { "helpers": ["helpers"] }
    try:
        config_file = lib50.config.get_config_filepath(dir)

        with open(config_file) as f:
            config = CONFIG_LOADER.load(f.read())
    except lib50.InvalidConfigError:
        raise Error("Failed to parse help50 config, please let sysadmins@cs50.harvard.edu know!")


    if isinstance(config, dict):
        options.update(config)

    if isinstance(options["helpers"], str):
        options["helpers"] = [options["helpers"]]

    return options


def load_helpers(helpers_dir):
    """ Download helpers to a local directory via lib50. """

    config = load_config(helpers_dir)
    for helper in config["helpers"]:
        with _syspath([str(helpers_dir)]):
            try:
                __import__(helper)
            except ImportError:
                raise Error("Failed to load helpers, please let sysadmins@cs50.harvard.edu know!")


def get_help(output):
    """
    Given an error message, try every helper registered with help50 and return the output of the
    first one that matches.
    """
    # Strip ANSI codes
    output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)

    for domain in HELPERS.keys():
        processed = output
        for pre in PREPROCESSORS.get(domain, []):
            processed = pre(processed)
        lines = processed.splitlines()
        for i in range(len(lines)):
            slice = lines[i:]
            for helper in HELPERS.get(domain, []):
                try:
                    before, after = helper(slice)
                except TypeError:
                    pass
                else:
                    return before, after
