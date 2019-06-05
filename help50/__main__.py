#!/usr/bin/env python
import contextlib
import io
import itertools
import importlib
import os
import re
import shlex
import shutil
import signal
import sys
import textwrap
import tempfile

from argparse import ArgumentParser, REMAINDER
import lib50
import requests
import termcolor
import pexpect

from . import HELPERS, PRE_HELPERS

lib50.api.LOCAL_PATH = "~/.local/share/help50"


@contextlib.contextmanager
def syspath(newpath):
    oldpath = sys.path
    sys.path = newpath
    try:
        yield
    finally:
        sys.path = oldpath


def load_config(dir):
    options = { "helpers": ["helpers"] }
    config_file = dir / ".cs50.yaml"

    with open(config_file) as f:
        config = lib50.config.load(f.read(), "help50")

    if isinstance(config, dict):
        options.update(config)

    if isinstance(options["helpers"], str):
        options["helpers"] = [options["helpers"]]

    return options


def load_helpers(slug, offline=False):
    helpers_dir = lib50.local(slug, "help50")
    config = load_config(helpers_dir)
    for helper in config["helpers"]:
        with syspath([str(helpers_dir)]):
            __import__(helper)



def get_help(output, *domains):
    if not domains:
        domains = HELPERS.keys()

    # Strip ANSI codes
    output = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", output)

    for domain in domains:
        lines = output
        for pre_helper in PRE_HELPERS.get(domain, []):
            lines = pre_helper(lines)
        lines = lines.splitlines()
        for helper in HELPERS.get(domain, []):
            try:
                before, after = helper(lines)
            except TypeError:
                pass
            else:
                return before, " ".join(after)


def render_help(help):
    if help is None:
        termcolor.cprint("help50 does not yet know how to help with this!", "yellow")
    else:
        for line in help[0]:
            termcolor.cprint(line, "grey", "on_yellow")
        print()
        termcolor.cprint(re.sub(r"`([^`]+)`", r"\033[1m\1\033[22m", help[1]), "yellow")


def main():
    def handler(signum, frame):
        """Return 1 on Ctrl-C"""
        print("")
        sys.exit(1)

    signal.signal(signal.SIGINT, handler)

    parser = ArgumentParser(description="A command-line tool that helps "
                                        "students understand error messages.")
    parser.add_argument("-i", "--interactive",
                        help="allow error messages to be written to "
                              "stdin interactively",
                        action="store_true")
    parser.add_argument("-s", "--slug", help="identifier indicating from where to download helpers", default="cs50/helpers/master")
    parser.add_argument("--offline", help="run help50 offline", action="store_true")
    parser.add_argument("command", nargs=REMAINDER,
                        default=[], help="command to be run")
    args = parser.parse_args()

    load_helpers(args.slug, args.offline)

    if args.command:
        # Capture stdout and stderr from process, and print it out
        with tempfile.TemporaryFile(mode="r+b") as temp:
            proc = pexpect.spawn(f"bash -lc \"{' '.join(shlex.quote(word) for word in args.command)}\"", env=os.environ)
            proc.logfile_read = temp
            proc.interact()
            proc.close()

            temp.seek(0)
            script = temp.read().decode().replace("\r\n", "\n")

    # Interactive stdin
    elif args.interactive:
        script = sys.stdin.read()

    # Non-interactive stdin
    elif not sys.stdin.isatty():
        with io.BytesIO() as iobytes:
            tee(sys.stdin.buffer, iobytes, sys.stdout.buffer)
            script = iobytes.getvalue().decode("utf-8")

    # Disallow interactive without `-i` input (as potentially confusing)
    else:
        print("Careful, you forgot to tell me with which command you "
              "need help!")
        sys.exit(1)

    termcolor.cprint("\nAsking for help...\n", "yellow")

    help = get_help(script)
    render_help(help)

    # data = {
        # "cmd": " ".join(sys.argv[1:]),
        # "format": "ans",
        # "script": script,
        # "username": os.environ.get("C9_USER")
    # }

    # # Read help50 url and from environment variable,
    # # defaulting to help.cs50.net
    # app_url = os.environ.get("APP_URL") or "https://help.cs50.net/"

    # # Get number of columns in terminal, defaulting to 80
    # columns, _ = shutil.get_terminal_size()
    # if columns == 0: columns = 80

    # # Connect to server and print response, showing error message if unable to
    # try:
        # # Connect to server
        # r = requests.post(app_url, data)
    # except requests.exceptions.RequestException:
        # termcolor.cprint(wrap("Ack, there seems to be a bug in help50! "
                              # "Please let sysadmins@cs50.harvard.edu know "
                              # "with which error you need help!",
                              # columns),
                         # "yellow", end="")
        # sys.exit(1)
    # else:
        # # Overwrite previous line with spaces
        # print("\r{}\r".format(" " * columns), end="")
        # termcolor.cprint(wrap(r.text.encode("utf-8").decode("unicode_escape"),
                              # columns),
                         # "yellow", end="")


def tee(input, *outputs):
    """Executes command, piping stdout and stderr to *outputs."""
    while True:
        try:
            byte = input.read(1)
        except EOFError:
            byte = None

        if not byte:
            break

        for output in outputs:
            output.write(byte)
            output.flush()


def wrap(lines, columns):
    """ Wraps a string to the specified number of columns,
        preserving blank lines.
    """
    return "\n".join(
        ("\n".join(textwrap.wrap(line, columns))
         for line in lines))


if __name__ == "__main__":
    main()
