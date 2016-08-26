import re
def help(lines):

    # is up to date.
    matches = re.search(r"^make: `(.+)' is up to date.", lines[0])
    if matches:
        after = [
            "Looks like you already compiled `{}` and haven't made any changes to `{}.c` since.".format(matches.group(1), matches.group(1)),
            "Or did you forget to save `{}.c` before running `make`?".format(matches.group(1))
        ]
        return (lines[0:1], after)

    # No rule to make target
    matches = re.search(r"^make: \*\*\* No rule to make target `(.+)'.  Stop.", lines[0])
    if matches:
        after = [
            "Do you actually have a file called `{}`.c?".format(matches.group(1)),
            "If using a Makefile, are you sure you have a target called `{}`?".format(matches.group(1))
        ]
        return (lines[0:1], after)
    
    # nothing to be done for
    matches = re.search(r"^make: Nothing to be done for `([^']+).c'.", lines[0])
    if matches:
        after = [
            "Try compiling your program with `make {}` rather than `make {}.c`.".format(matches.group(1), matches.group(1))
        ]
        return (lines[0:1], after)
