#!/usr/bin/env python
import io
import os
import re
import shlex
import shutil
import sys
import textwrap
import traceback

from argparse import ArgumentParser, REMAINDER
import lib50
import termcolor
import pexpect

from . import __version__, internal, Error

ON_WINDOWS = os.name == "nt"

if ON_WINDOWS:
    # Fix termcolor colors on Windows
    import colorama
    colorama.init()

try:
    TERMINAL_COLS = shutil.get_terminal_size()[0]
except Exception:
    TERMINAL_COLS = 80


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


def cprint_wrapped(text, *args, **kwargs):
    """
    Print `text` via cprint, ensuring that lines are no longer than `width`.
    `text` should not contain any newlines (if it does, they will be removed by
    textwrap.fill
    """
    width = kwargs.pop("width", TERMINAL_COLS)
    termcolor.cprint(textwrap.fill(text, width=width), *args, **kwargs)


def render_help(help):
    """
    Display help message to student.

    `help` should be a 2-tuple whose first element is the part of the error
    message that is being translated and whose second element is the
    translation itself.
    """
    if help is None:
        cprint_wrapped("Sorry, help50 does not yet know how to help with this!", "yellow")
    else:
        for line in help[0]:
            cprint_wrapped(line, "grey", "on_yellow")
        print()
        cprint_wrapped(re.sub(r"`([^`]+)`", r"\033[1m\1\033[22m", " " .join(help[1])), "yellow")


def main():
    parser = ArgumentParser(prog="help50",
                            description="A command-line tool that helps "
                                        "students understand error messages.")
    parser.add_argument("-s", "--slug", help="identifier indicating from where to download helpers", default="cs50/helpers/main")
    parser.add_argument("-d", "--dev", help="slug will be treated as a local path, useful for developing helpers (implies --verbose)", action="store_true")
    parser.add_argument("-v", "--verbose", help="display the full tracebacks of any errors", action="store_true")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("command", nargs=REMAINDER,
                        default=[], help="command to be run")
    args = parser.parse_args()

    if args.dev:
        args.verbose = True

    excepthook.verbose = args.verbose

    if args.command:
        command = " ".join(shlex.quote(word) for word in args.command)
        script = b""

        # pty isn't supported on Windows
        if ON_WINDOWS:
            import subprocess
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for b in iter(lambda: proc.stdout.read(1), b""):
                script += b
                sys.stdout.buffer.write(b)
                sys.stdout.flush()
        else:
            import pty
            def master_read(fd):
                nonlocal script
                data = os.read(fd, 1024)
                script += data
                return data

            old_env = os.environ.copy()

            # Hack to prevent some programs from wrapping their error messages
            os.environ.update({"COLUMNS": "5050"})
            try:
                # Run the process in a pseudo-terminal e.g., to preserve colored output
                pty.spawn(["bash", "-O", "expand_aliases", "-lc", command], master_read)
            finally:
                os.environ.clear()
                os.environ.update(old_env)

        script = script.decode().replace("\r\n", "\n")
    else:
        raise Error("Careful, you forgot to tell me with which command you "
                    "need help!")
    print()
    cprint_wrapped("Asking for help...", "yellow")
    print()

    try:
        helpers_dir = args.slug if args.dev else lib50.local(args.slug)
    except lib50.Error:
        raise Error("Failed to fetch helpers, please ensure that you are connected to the internet!")

    internal.load_helpers(helpers_dir)
    render_help(internal.get_help(script))


if __name__ == "__main__":
    main()
