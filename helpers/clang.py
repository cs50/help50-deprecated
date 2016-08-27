import re
def help(lines):
 
    # control reaches end of non-void function
    matches = re.search(r"control (may)?reach(es)? end of non-void function", lines[0])
    if matches:
        after = ["Ensure that your function will always return a value. If your function is not meant to return a value, try changing its return type to `void`."]
        return (lines[0:1], after)

    # data argument not used by format string
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): data argument not used by format string", lines[0])
    if matches:
        after = [
            "You have more arguments in your formatted string on line {} of `{}` than you have format codes.".format(matches.group(2), matches.group(1)),
            "Make sure that the number of format codes equals the number of additional arguments.",
            "Try either adding format code(s) or removing argument(s)."
        ]
        return (lines[0:1], after)

    # expected }
    matches = re.search(r"error: expected '}'", lines[0])
    if matches:
        after = ["Make sure that all opening brace symbols `{` are matched with a closing brace `}`."]
        return (lines[0:1], after)
    
    # expected )
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected '\)'", lines[0])
    if matches:
        after = [
            "Make sure that all opening parentheses `(` are matched with a closing parenthesis `)` in {}.".format(matches.group(1)),
            "In particular, check to see if you are missing a closing parenthesis on line {} of {}.".format(matches.group(2), matches.group(1))
        ]
        return (lines[0:1], after)

    # expected ; after declaration
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected ';' (?:after\sexpression|at\send\sof\sdeclaration)", lines[0])
    if matches:
        after = ["Try including a semicolon at the end of line {} of `{}`.".format(matches.group(2), matches.group(1))]
        return (lines[0:1], after)

    # expected ';' in 'for' statement
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected ';' in 'for' statement specifier", lines[0])
    if matches:
        after = ["Be sure to separate the three components of the 'for' loop on line {} of `{}` with semicolons.".format(matches.group(2), matches.group(1))]
        return (lines[0:1], after)

    # extra tokens at end of #include directive
    matches = re.search(r"^([^:]+):(\d+):(\d+): (?:warning|error): extra tokens at end of #include directive", lines[0])
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
    matches = re.search(r"^([^:]+):(\d+):(\d+): (?:warning|error): implicit declaration of function '([^']+)' is invalid", lines[0])
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

    # incompatible conversion
    matches = re.search(r"incompatible ([^']+) to ([^']+) conversion", lines[0])
    if matches:
        after = ["By \"incompatible conversion\", `clang` means that you are assigning a value to a variable of a different type. Try ensuring that your value is of type `{}`.".format(matches.group(2))]
        return (lines[0:1], after)

    # incorrect format code
    matches = re.search(r"^([^:]+):(\d+):\d+: error: format specifies type '[^:]+' but the argument has type '[^:]+'", lines[0])
    if matches:
        after = ["Be sure to use the correct format code (%i for integers, %f for floating point values, %s for strings) in your string format statement on line {} of `{}`.".format(matches.group(2), matches.group(1))]
        return (lines[0:1], after)

    # invalid preprocessing directive
    matches = re.search(r"^([^:]+):(\d+):\d+: error: invalid preprocessing directive", lines[0])
    if matches:
        after = ["By \"invalid preprocesing directive\", `clang` means that you've used a preprocessor command (a command beginning with #) on line {} of `{}` that is not recognized.".format(matches.group(2), matches.group(1))]
        if len(lines) >= 2:
            directive = re.search(r"^([^' ]+)", lines[1])
            if directive:
                after.append("Check to make sure that `{}` is a valid directive (like `#include`) and is spelled correctly.".format(directive.group(1)))
                return (lines[0:2], after)
        return (lines[0:1], after)
  
    # more '%' conversions than data arguments
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): more '%' conversions than data arguments", lines[0])
    if matches:
        after = [
            "You have too many format codes (e.g. %i or %s) in your formatted string on line {} of `{}`.".format(matches.group(2), matches.group(1)),
            "Make sure that the number of format codes equals the number of additional arguments.",
            "Try either removing format code(s) or adding additional argument(s)"
        ]
        return (lines[0:1], after)
   
    # result of assignment as a condition
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): using the result of an assignment as a condition without parentheses", lines[0])
    if matches:
        after = ["When checking for equality in the condition on line {} of `{}`, try using a double equals sign (`==`) instead of a single equals sign (`=`).".format(matches.group(1), matches.group(2))]
        return (lines[0:1], after)

    # undeclared identifier
    matches = re.search(r"use of undeclared identifier '([^']+)'", lines[0])
    if matches:
        after = ["By \"undeclared identifier,\" `clang` means you've used a name `{}` which hasn't been defined.".format(matches.group(1))]
        if matches.group(1) in ["true", "false", "bool", "string"]:
            after.append("Did you forget to `#include <cs50.h>` (in which `{}` is defined) atop your file?".format(matches.group(1)))
        else:
            after.append("If you mean to use `{}` as a variable, make sure to declare it by specifying its type, and check that the variable name is spelled correctly.".format(matches.group(1)))
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

    # unknown type name 'include'
    matches = re.search(r"unknown type name 'include'", lines[0])
    if matches:
        after = ["Try including header files via `#include` rather than just `include`."]
        return (lines[0:2], after)

    # unused variable
    matches = re.search(r"unused variable '([^']+)'", lines[0])
    if matches:
        after = ["It seems that the variable `{}` is never in your program. Try either removing it altogether or using it.".format(matches.group(1))]
        return (lines[0:1], after)
  