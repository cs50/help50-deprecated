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
        termcolor.cprint(re.sub(r"`([^`]+)`", r"\033[1m\1\033[22m", help[1]), "yellow")


def tee(input, *outputs):
    """Copies input to all outputs byte-by-byte"""
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

def main():
    parser = ArgumentParser(prog="help50",
                            description="A command-line tool that helps "
                                        "students understand error messages.")
    parser.add_argument("-i", "--interactive",
                        help="allow error messages to be written to "
                              "stdin interactively",
                        action="store_true")
    parser.add_argument("-s", "--slug", help="identifier indicating from where to download helpers", default="cs50/helpers/master")
    parser.add_argument("-v", "--verbose", help="display the full tracebacks of any errors", action="store_true")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("command", nargs=REMAINDER,
                        default=[], help="command to be run")
    args = parser.parse_args()

    excepthook.verbose = args.verbose

    internal.load_helpers(args.slug)

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
        raise Error("Careful, you forgot to tell me with which command you "
                    "need help!")


    termcolor.cprint("\nAsking for help...\n", "yellow")

    render_help(internal.get_help(script))


if __name__ == "__main__":
    main()
