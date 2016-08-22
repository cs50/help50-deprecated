import re
def help(lines):

    # is up to date.
    matches = re.search(r"^make: `(.+)' is up to date.", lines[0])
    if matches:
        after = [
            "Looks like you already compiled `{}` and haven't made any changes to `{}.c` since.".format(matches.group(1), matches.group(1)),
            "Or did you forget to save `{}.c` before running `make`?".format(matches.group(1)),
        ]
        return (lines[0:1], after)
