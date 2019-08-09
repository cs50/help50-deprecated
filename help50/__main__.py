#!/usr/bin/env python
import io
import os
import re
import shlex
import sys
import tempfile
import traceback

from argparse import ArgumentParser, REMAINDER
import lib50
import termcolor
import pexpect

from . import __version__, internal, Error


def excepthook(cls, exc, tb):
    if (issubclass(cls, lib50.Error) or issubclass(cls, Error)) and exc.args:
        termcolor.cprint(str(exc), "red", file=sys.stderr)
    elif issubclass(cls, FileNotFoundError):
        termcolor.cprint(f"{exc.filename} not found", "red", file=sys.stderr)
    elif issubclass(cls, KeyboardInterrupt):
        print()
    elif not issubclass(cls, Exception):
        return
    else:
        termcolor.cprint("Sorry, something's wrong! Let sysadmins@cs50.harvard.edu know!", "red", file=sys.stderr)

    if excepthook.verbose:
        traceback.print_exception(cls, exc, tb)

    sys.exit(1)


excepthook.verbose = True
sys.excepthook = excepthook


def render_help(help):
    """
    Display help message to student.

    `help` should be a 2-tuple whose first element is the part of the error
    message that is being translated and whose second element is the
    translation itself.
    """
    if help is None:
        termcolor.cprint("Sorry, help50 does not yet know how to help with this!", "yellow")
    else:
        for line in help[0]:
            termcolor.cprint(line, "grey", "on_yellow")
        print()
        termcolor.cprint(re.sub(r"`([^`]+)`", r"\033[1m\1\033[22m", " " .join(help[1])), "yellow")


def main():
    parser = ArgumentParser(prog="help50",
                            description="A command-line tool that helps "
                                        "students understand error messages.")
    parser.add_argument("-s", "--slug", help="identifier indicating from where to download helpers", default="cs50/helpers/master")
    parser.add_argument("-d", "--dev", help="slug will be treated as a local path, useful for developing helpers (implies --verbose)", action="store_true")
    parser.add_argument("-i", "--interactive", help="read command output from stdin instead of running a command", action="store_true")
    parser.add_argument("-v", "--verbose", help="display the full tracebacks of any errors", action="store_true")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("command", nargs=REMAINDER,
                        default=[], help="command to be run")
    args = parser.parse_args()

    if args.dev:
        args.verbose = True

    excepthook.verbose = args.verbose


    if args.interactive:
        script = sys.stdin.read()
    elif args.command:
        # Capture stdout and stderr from process, and print it out
        with tempfile.TemporaryFile(mode="r+b") as temp:
            env = os.environ.copy()
            # Hack to prevent some programs from wrapping their error messages
            env["COLUMNS"] = "5050"
            proc = pexpect.spawn(f"bash -lc \"{' '.join(shlex.quote(word) for word in args.command)}\"", env=env)
            proc.logfile_read = temp
            proc.interact()
            proc.close()

            temp.seek(0)
            script = temp.read().decode().replace("\r\n", "\n")
    else:
        raise Error("Careful, you forgot to tell me with which command you "
                    "need help!")
    termcolor.cprint("\nAsking for help...\n", "yellow")

    try:
        helpers_dir = args.slug if args.dev else lib50.local(args.slug)
    except lib50.Error:
        raise Error("Failed to fetch helpers, please ensure that you are connected to the internet!")

    internal.load_helpers(helpers_dir)
    render_help(internal.get_help(script))


if __name__ == "__main__":
    main()
