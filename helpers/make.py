import re
def help(lines):

    # $ make foo
    # make: `foo' is up to date.
    matches = re.search(r"^make: `(.+)' is up to date.", lines[0])
    if matches:
        after = [
            "Looks like you already compiled `{}` and haven't made any changes to `{}.c` since.".format(matches.group(1), matches.group(1)),
            "Or did you forget to save `{}.c` before running `make`?".format(matches.group(1))
        ]
        return (lines[0:1], after)

    # $ make foo
    # make: *** No rule to make target `foo'.  Stop.
    matches = re.search(r"^make: \*\*\* No rule to make target `(.+)'.  Stop.", lines[0])
    if matches:
        after = [
            "Do you actually have a file called `{}`.c?".format(matches.group(1)),
            "If using a Makefile, are you sure you have a target called `{}`?".format(matches.group(1))
        ]
        return (lines[0:1], after)
    
    # $ make foo.c
    # make: Nothing to be done for `foo.c'.
    matches = re.search(r"^make: Nothing to be done for `([^']+).c'.", lines[0])
    if matches:
        after = [
            "Try compiling your program with `make {}` rather than `make {}.c`.".format(matches.group(1), matches.group(1))
        ]
        return (lines[0:1], after)
    
    # $ make foo
    # clang -ggdb3 -O0 -std=c11 -Wall -Werror -Wshadow foo.c -lcs50 -lm -o foo
    matches = re.search(r"^clang", lines[0])
    if matches and len(lines) == 1 and "error:" not in lines[0]:
        after = [
            "Looks like your program compiles successfully!"
        ]
        return (lines[0:1], after)
