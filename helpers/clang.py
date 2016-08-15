import re
def help(lines):

    # extra tokens at end of #include directive
    matches = re.search(r"^([^:]+):(\d+):(\d+): warning: extra tokens at end of #include directive", lines[0])
    if matches:
        after = [
            "You seem to have an error in `{}` on line {} at character {}.".format(matches.group(1), matches.group(2), matches.group(3)),
            "By \"extra tokens\", `clang` means that you have one or more extra characters on that line that you shouldn't."
        ]
        if len(lines) >= 3 and re.search(r"^\s*\^", lines[2]):
            token = lines[1][lines[2].index("^")]
            if token == ";":
                after.append("Try removing the semicolon at the end of that line.")
            else:
                after.append("Try removing the `{}` at the end of that line.".format(token))
            return (lines[0:3], after)
        return (lines[0:1], after)

    # implicit declaration of function
    matches = re.search(r"^([^:]+):(\d+):(\d+): warning: implicit declaration of function '([^']+)' is invalid", lines[0])
    if matches:
        after = [
            "You seem to have an error in `{}` on line {} at character {}.".format(matches.group(1), matches.group(2), matches.group(3)),
            "By \"implicit declaration of function '{}'\", `clang` means that it doesn't recognize `{}`.".format(matches.group(4), matches.group(4)),
            "Did you forget to `#include` the header file in which `{}` is declared) atop your file?".format(matches.group(4)),
            "Did you forget to declare a prototype for `{}` atop `{}`?".format(matches.group(4), matches.group(1))
        ]
        return (lines[0:1], after)

    # implicitly declaring library function
    matches = re.search(r"implicitly declaring library function '([^']+)'", lines[0])
    if matches:
        if (matches.group(1) == "printf"):
            after = ["Did you forget to `#include <stdio.h>` (in which `printf` is declared) atop your file?"]
        else:
            after = ["Did you forget to `#include` the header file in which `{}` is declared) atop your file?".format(matches.group(1))]
        return (lines[0:1], after)

    # undefined reference
    matches = re.search(r"undefined reference to `([^']+)'", lines[0])
    if matches:
        after = ["By \"undefined reference,\" `clang` means that you've called a function, `{}`, that doesn't seem to be implemented. If that function has, in fact, been implemented, odds are you've forgotten to tell `clang` to \"link\" against the file that implements `{}`.".format(matches.group(1), matches.group(1))]
        if matches.group(1) in ["eprintf", "get_char", "get_double", "get_float", "get_int", "get_long", "get_long_long", "get_string"]:
            after.append("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{}`?".format(matches.group(1)))
        elif matches.group(1) in ["GetChar", "GetDouble", "GetFloat", "GetInt", "GetLong", "GetLongLong", "GetString"]:
            after.append("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{}`?".format(matches.group(1)))
        elif matches.group(1) == "crypt":
            after.append("Did you forget to compile with -lcrypt in order to link against the crypto library, which implemens `crypt`?")
        else:
            after.append("Did you forget to compile with `-lfoo`, where `foo` is the library that defines `{}`?".format(matches.group(1)))
        return (lines[0:1], after)
