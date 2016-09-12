import re
from tools import *

def help(lines):

    # $ clang foo.c
    # foo.c:13:25: error: adding 'int' to a string does not append to the string [-Werror,-Wstring-plus-int]
    matches = re.search(r"^([^:]+):(\d+):\d+: error: adding '(.+)' to a string does not append to the string", lines[0])
    if matches:
        response = ["Careful, you can't concatenate values and strings in C using the `+` operator, as you seem to be trying to do on line {} of `{}`.".format(matches.group(2), matches.group(1))]
        if len(lines) >= 2 and re.search(r"printf\s*\(", lines[1]):
            response.append("Odds are you want to provide `printf` with a format code for that value and pass that value to `printf` as an argument.")
            return (2, response)
        return (1, response)
    
    # $ clang foo.c
    # foo.c:6:21: error: array subscript is not an integer
    #     printf("%i\n", x["28"]);
    #                     ^~~~~ 
    matches = re.search(r"^([^:]+):(\d+):\d+: error: array subscript is not an integer", lines[0])
    if matches:
        array = var_extract(lines[1:3], left_aligned=False)
        index = tilde_extract(lines[1:3])
        if array and index:
            response = [
                "Looks like you're trying to access an element of the array `{}` on line {} of `{}`, but your index `{}` is not of type `int`.".format(array, matches.group(2), matches.group(1), index)    
            ]
        else:
            response = [
                "Looks like you're trying to access an element of an array on line {} of `{}`, but your index is not of type `int`.".format(matches.group(2), matches.group(1))
            ]
        response.append("Make sure your index (the value between square brackets) is an `int`.")
        if len(lines) >= 2 and re.search(r"[.*]", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:1: error: control reaches end of non-void function [-Werror,-Wreturn-type]
    #
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:7:1: error: control may reach end of non-void function [-Werror,-Wreturn-type]
    matches = re.search(r"control (may)?reach(es)? end of non-void function", lines[0])
    if matches:
        response = ["Ensure that your function will always return a value. If your function is not meant to return a value, try changing its return type to `void`."]
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:29: error: data argument not used by format string [-Werror,-Wformat-extra-args]
    #    printf("%d %d", 27, 28, 29);
    #           ~~~~~~~          ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): data argument not used by format string", lines[0])
    if matches:
        response = [
            "You have more arguments in your formatted string on line {} of `{}` than you have format codes.".format(matches.group(2), matches.group(1)),
            "Make sure that the number of format codes equals the number of additional arguments.",
            "Try either adding format code(s) or removing argument(s)."
        ]
        if len(lines) >= 2 and re.search(r"%", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:8: error: declaration shadows a local variable [-Werror,-Wshadow]
    #    int x = 28;
    #        ^
    #
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:20: error: declaration shadows a local variable [-Werror,-Wshadow]
    #    for (int i = 0, i < 28, i++)
    #                    ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): declaration shadows a local variable", lines[0])
    if matches:
        response = [
            "On line {} of `{}`, it seems that you're trying to create a new variable that has already been created.".format(matches.group(2), matches.group(1))
        ]

        # check to see if declaration shadowing is due to for loop with commas instead of semicolons
        if len(lines) >= 2:
            for_loop = re.search(r"^\s*for\s*\(", lines[1])
            if for_loop:
                response.append("If you meant to create a `for` loop, be sure that each part of the `for` loop is separated with a semicolon rather than a comma.")
                if (len(lines) >= 3 and re.search(r"^\s*\^$", lines[2])):
                    return (3, response)
                return (2, response)

        # see if we can get the line number of the previous declaration of the variable
        prev_declaration_file = None
        prev_declaration_line = None
        if len(lines) >= 4:
            prev = re.search(r"^([^:]+):(\d+):\d+: note: previous declaration is here", lines[3])
            if prev:
                prev_declaration_line = prev.group(2)
                prev_declaration_file = prev.group(1)

        omit_suggestion = "If you meant to use the variable you've already declared previously"
        if prev_declaration_line and prev_declaration_file:
            omit_suggestion += " (on line {} of `{}`)".format(prev_declaration_line, prev_declaration_file)
        omit_suggestion += ", try getting rid of the data type of the variable on line {} of `{}`. You only need to include the data type when you first declare a variable.".format(matches.group(2), matches.group(1))
        response.append(omit_suggestion)
        response.append("Otherwise, if you did mean to declare a new variable, try changing its name to a name that hasn't been used yet.")
        
        if len(lines) >= 4 and prev_declaration_line != None:
            return (6, response) if len(lines) >= 6 and re.search(r"^\s*\^$", lines[5]) else (4, response)
        if len(lines) >= 2:
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:1: error: expected identifier or '('
    # do
    # ^
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected identifier or '\('", lines[0])
    if matches:
        response = [
            "Looks like `clang` is having some trouble understanding where your functions start and end in your code.",
            "Are you defining a function (like `main` or some other function) somewhere just before line {} of `{}`?".format(matches.group(2), matches.group(1)),
            "If so, make sure the function header (the line that introduces the name of the function) doesn't end with a semicolon.",
            "Also check to make sure that all of the code for your function is inside of curly braces."
        ]
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:3:12: error: expected parameter declarator
    # int square(28);
    #            ^
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected parameter declarator", lines[0])
    if matches:
        response = [
            "If you're trying to call a function on line {} of `{}`, be sure that you're calling it inside of curly braces within a function. Also check that the function's header (the line introducing the function's name) doesn't end in a semicolon.".format(matches.group(2), matches.group(1)),
            "Alternatively, if you're trying to declare a function or prototype on line {} of `{}`, be sure each argument to the function is formatted as a data type followed by a variable name.".format(matches.group(2), matches.group(1))
        ]
        if len(lines) >= 3 and re.search(r"^\s*\^$", lines[2]):
            return (3, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:9:2: error: expected '}'
    # }
    #  ^
    matches = re.search(r"error: expected '}'", lines[0])
    if matches:
        response = ["Make sure that all opening brace symbols `{` are matched with a closing brace `}`."]
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:8: error: expected '(' after 'if'
    #     if x == 28
    #        ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): expected '\(' after 'if'", lines[0])
    if matches:
        response = [
            "In your `if` statement on line {} of `{}`, be sure that you're enclosing the condition you're testing within parentheses.".format(matches.group(2), matches.group(1))
        ]
        if len(lines) >= 2 and re.search(r"if\s*\(", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:1: error: expected ')'
    # }
    # ^
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected '\)'", lines[0])
    if matches:
        # assume that the line number for the matching ')' is the line that generated the error
        match_line = matches.group(2)
        n = 1

        # if there's a note on which '(' to match, use that line number instead
        if (len(lines) >= 4):
            parens_match = re.search(r"^([^:]+):(\d+):\d+: note: to match this '\('", lines[3])
            if parens_match:
                match_line = parens_match.group(2)
                n = 4

        response = [
            "Make sure that all opening parentheses `(` are matched with a closing parenthesis `)` in {}.".format(matches.group(1)),
            "In particular, check to see if you are missing a closing parenthesis on line {} of {}.".format(match_line, matches.group(1))
        ]
        return (n, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:27: error: expected ';' after expression
    #    printf("hello, world!")
    #                           ^
    #                           ;
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected ';' (?:after expression|at end of declaration|after do\/while statement)", lines[0])
    if matches:
        response = ["Try including a semicolon at the end of line {} of `{}`.".format(matches.group(2), matches.group(1))]
        if len(lines) >= 3 and re.search(r"^\s*\^$", lines[2]):
            if len(lines) >= 4 and re.search(r"^\s*;$", lines[3]):
                return (4, response)
            return (3, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:22: error: expected ';' in 'for' statement specifier
    #    for (int i = 0, i < 28, i++)
    #                      ^
    matches = re.search(r"^[^:]+:(\d+):\d+: error: expected ';' in 'for' statement specifier", lines[0])
    if matches:
        response = ["Be sure to separate the three components of the 'for' loop on line {} with semicolons.".format(matches.group(1))]
        if len(lines) >= 2 and re.search(r"for\s*\(", lines[1]):
            return (2, response)
        return (1, response)
    
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:28:28: error: expected expression
    matches = re.search(r"^([^:]+):(\d+):\d+: error: expected expression", lines[0])
    if matches:
        response = [
            "Not quite sure how to help, but focus your attention on line {} of `{}`!".format(matches.group(2), matches.group(1))
        ]
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:1:19: error: extra tokens at end of #include directive [-Werror,-Wextra-tokens]
    # #include <stdio.h>;
    #                   ^
    matches = re.search(r"^([^:]+):(\d+):(\d+): (?:warning|error): extra tokens at end of #include directive", lines[0])
    if matches:
        response = [
            "You seem to have an error in `{}` on line {} at character {}.".format(matches.group(1), matches.group(2), matches.group(3)),
            "By \"extra tokens\", `clang` means that you have one or more extra characters on that line that you shouldn't."
        ]
        if len(lines) >= 3 and re.search(r"^\s*\^", lines[2]):
            token = lines[1][lines[2].index("^")]
            if token == ";":
                response.append("Try removing the semicolon at the end of that line.")
            else:
                response.append("Try removing the `{}` at the end of that line.".format(token))
            return (2, response)
        return (1, response)
    
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:1:10: fatal error: 'studio.h' file not found
    # #include <studio.h>
    #          ^
    matches = re.search(r"^([^:]+):(\d+):\d+: fatal error: '(.*)' file not found", lines[0])
    if matches:
        response = [
            "Looks like you're trying to `#include` a file (`{}`) on line {} of `{}` which does not exist.".format(matches.group(3), matches.group(2), matches.group(1))
        ]
        if matches.group(3) in ["studio.h"]:
            response.append("Did you mean to `#include <stdio.h>` (without the `u`)?")
        else:
            response.append("Check to make sure you spelled the filename correctly.")
            
        if len(lines) >= 2 and re.search(r"#include", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # foo.c:6:16: error: format string is not a string literal (potentially insecure) [-Werror,-Wformat-security]
    # printf(c);
    # ^ 1 error generated.
    matches = re.search(r"^([^:]+):(\d+):\d+: error: format string is not a string literal", lines[0])
    if matches and len(lines) >= 3 and re.search(r"^\s*\^", lines[2]):
        file, line = matches.groups()
        matches = re.search(r"^(.?printf|.?scanf)\s*\(", lines[1][lines[2].index("^"):])
        print(lines[1][lines[2].index("^"):])
        if matches:
            response = ["The first argument to `{}` on line {} of `{}` should be a double-quoted string.".format(matches.group(1), line, file)]
            return (2, response)
        
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:12:15: error: if statement has empty body [-Werror,-Wempty-body]
    #   if (n > 0);
    #             ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): (if statement|while loop|for loop) has empty body", lines[0])
    if matches:
        response = [
            "Try removing the semicolon directly after the closing parentheses of the `{}` on line {} of `{}`.".format(matches.group(3),matches.group(2), matches.group(1))
        ]
        if len(lines) >= 2 and re.search(r"if\s*\(", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:12: error: implicit declaration of function 'get_int' is invalid in C99 [-Werror,-Wimplicit-function-declaration]
    #    int x = get_int();
    #            ^
    matches = re.search(r"^([^:]+):(\d+):(\d+): (?:warning|error): implicit declaration of function '([^']+)' is invalid", lines[0])
    if matches:
        response = [
            "You seem to have an error in `{}` on line {} at character {}.".format(matches.group(1), matches.group(2), matches.group(3)),
            "By \"implicit declaration of function '{}'\", `clang` means that it doesn't recognize `{}`.".format(matches.group(4), matches.group(4))
        ]
        if matches.group(4) in ["eprintf", "get_char", "get_double", "get_float", "get_int", "get_long", "get_long_long", "get_string", "GetChar", "GetDouble", "GetFloat", "GetInt", "GetLong", "GetLongLong", "GetString"]:
            response.append("Did you forget to `#include <cs50.h>` (in which `{}` is declared) atop your file?".format(matches.group(4)))
        else:
            response.append("Did you forget to `#include` the header file in which `{}` is declared atop your file?".format(matches.group(4)))
            response.append("Did you forget to declare a prototype for `{}` atop `{}`?".format(matches.group(4), matches.group(1)))
            
        if len(lines) >= 2 and re.search(matches.group(4), lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:3:4: error: implicitly declaring library function 'printf' with type 'int (const char *, ...)' [-Werror]
    #    printf("hello, world!");
    #    ^
    matches = re.search(r"implicitly declaring library function '([^']+)'", lines[0])
    if matches:
        if (matches.group(1) == "printf"):
            response = ["Did you forget to `#include <stdio.h>` (in which `printf` is declared) atop your file?"]
        else:
            response = ["Did you forget to `#include` the header file in which `{}` is declared) atop your file?".format(matches.group(1))]
            
        if len(lines) >= 2 and re.search(r"printf\s*\(", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:3:8: error: incompatible pointer to integer conversion initializing 'int' with an expression of type 'char [3]'
    #       [-Werror,-Wint-conversion]
    #    int x = "28";
    #        ^   ~~~~
    matches = re.search(r"incompatible ([^']+) to ([^']+) conversion", lines[0])
    if matches:
        response = ["By \"incompatible conversion\", `clang` means that you are assigning a value to a variable of a different type. Try ensuring that your value is of type `{}`.".format(matches.group(2))]
        if len(lines) >= 2 and re.search(r"=", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:19: error: format specifies type 'int' but the argument has type 'char *' [-Werror,-Wformat]
    #    printf("%d\n", "hello!");
    #            ~~     ^~~~~~~~
    #            %s
    matches = re.search(r"^[^:]+:(\d+):\d+: error: format specifies type '[^:]+' but the argument has type '[^:]+'", lines[0])
    if matches:
        response = ["Be sure to use the correct format code (%i for integers, %f for floating point values, %s for strings) in your string format statement on line {}.".format(matches.group(1))]
        if len(lines) >= 3 and re.search(r"\^", lines[2]):
            if len(lines) >= 4 and re.search(r"%", lines[3]):
                return (4, response)
            return (3, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:1:2: error: invalid preprocessing directive
    # #incalude <stdio.h>
    #  ^
    matches = re.search(r"^[^:]+:(\d+):\d+: error: invalid preprocessing directive", lines[0])
    if matches:
        response = ["By \"invalid preprocesing directive\", `clang` means that you've used a preprocessor command on line {} (a command beginning with #) that is not recognized.".format(matches.group(1))]
        if len(lines) >= 2:
            directive = re.search(r"^([^' ]+)", lines[1])
            if directive:
                response.append("Check to make sure that `{}` is a valid directive (like `#include`) and is spelled correctly.".format(directive.group(1)))
                return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:16: error: more '%' conversions than data arguments [-Werror,-Wformat]
    #    printf("%d %d\n", 28);
    #               ~^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): more '%' conversions than data arguments", lines[0])
    if matches:
        response = [
            "You have too many format codes (e.g. %i or %s) in your formatted string on line {} of `{}`.".format(matches.group(2), matches.group(1)),
            "Make sure that the number of format codes equals the number of additional arguments.",
            "Try either removing format code(s) or adding additional argument(s)"
        ]
        if len(lines) >= 2 and re.search(r"%", lines[1]):
            return (2, response)
        return (1, response)
    
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:14: error: result of comparison against a string literal is unspecified (use strncmp instead) [-Werror,-Wstring-compare]
    #     if (word < "twenty-eight")
    #              ^ ~~~~~~~~~~~~~~
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): result of comparison against a string literal is unspecified", lines[0])
    if matches:
        response = [
            "You seem to be trying to compare two strings on line {} of `{}`".format(matches.group(2), matches.group(1)),
            "You can't compare two strings the same way you would compare two numbers (with `<`, `>`, etc.).",
            "Did you mean to compare two characters instead? If so, try using single quotation marks around characters instead of double quotation marks.",
            "If you need to compare two strings, try using the `strcmp` function declared in `string.h`."
        ]
        if len(lines) >= 2:
            return (2, response)
        return (1, response)
    
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:3:1: error: type specifier missing, defaults to 'int' [-Werror,-Wimplicit-int]
    # square (int x) {
    # ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): type specifier missing, defaults to 'int'", lines[0])
    if matches:
        response = [
            "Looks like you're trying to declare a function on line {} of `{}`.".format(matches.group(2), matches.group(1)),
            "Be sure that when you're declaring a function, you specify its return type just before the name of the function."
        ]
        if len(lines) >= 3 and re.search(r"^\s*\^$", lines[2]):
            return (3, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:10: error: using the result of an assignment as a condition without parentheses [-Werror,-Wparentheses]
    #    if (x = 28)
    #        ~~^~~~
    matches = re.search(r"^[^:]+:(\d+):\d+: (?:warning|error): using the result of an assignment as a condition without parentheses", lines[0])
    if matches:
        response = ["When checking for equality in the condition on line {}, try using a double equals sign (`==`) instead of a single equals sign (`=`).".format(matches.group(1))]
        if len(lines) >= 2 and re.search(r"if\s*\(", lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:5:4: error: use of undeclared identifier 'x'
    #    x = 28;
    #    ^
    matches = re.search(r"use of undeclared identifier '([^']+)'", lines[0])
    if matches:
        response = ["By \"undeclared identifier,\" `clang` means you've used a name `{}` which hasn't been defined.".format(matches.group(1))]
        if matches.group(1) in ["true", "false", "bool", "string"]:
            response.append("Did you forget to `#include <cs50.h>` (in which `{}` is defined) atop your file?".format(matches.group(1)))
        else:
            response.append("If you mean to use `{}` as a variable, make sure to declare it by specifying its type, and check that the variable name is spelled correctly.".format(matches.group(1)))
        if len(lines) >= 2 and re.search(matches.group(1), lines[1]):
            return (2, response)
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:(.text+0x9): undefined reference to `get_int'
    matches = re.search(r"undefined reference to `([^']+)'", lines[0])
    if matches:
        response = ["By \"undefined reference,\" `clang` means that you've called a function, `{}`, that doesn't seem to be implemented. If that function has, in fact, been implemented, odds are you've forgotten to tell `clang` to \"link\" against the file that implements `{}`.".format(matches.group(1), matches.group(1))]
        if matches.group(1) in ["eprintf", "get_char", "get_double", "get_float", "get_int", "get_long", "get_long_long", "get_string"]:
            response.append("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{}`?".format(matches.group(1)))
        elif matches.group(1) in ["GetChar", "GetDouble", "GetFloat", "GetInt", "GetLong", "GetLongLong", "GetString"]:
            response.append("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{}`?".format(matches.group(1)))
        elif matches.group(1) == "crypt":
            response.append("Did you forget to compile with -lcrypt in order to link against the crypto library, which implemens `crypt`?")
        else:
            response.append("Did you forget to compile with `-lfoo`, where `foo` is the library that defines `{}`?".format(matches.group(1)))
        return (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:1:1: error: unknown type name 'include'
    # include <stdio.h>
    # ^
    matches = re.search(r"unknown type name 'include'", lines[0])
    if matches:
        response = ["Try including header files via `#include` rather than just `include`."]
        return (2, response) if len(lines) >= 2 else (1, response)

    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:9: error: unused variable 'x' [-Werror,-Wunused-variable]
    #     int x = 28;
    #         ^
    matches = re.search(r"unused variable '([^']+)'", lines[0])
    if matches:
        response = ["It seems that the variable `{}` is never in your program. Try either removing it altogether or using it.".format(matches.group(1))]
        return (1, response)
    
    # $ clang foo.c
    # /tmp/foo-1ce1b9.o: In function `main':
    # foo.c:6:20: error: variable 'x' is uninitialized when used here [-Werror,-Wuninitialized]
    #     printf("%d\n", x);
    #                    ^
    matches = re.search(r"^([^:]+):(\d+):\d+: (?:warning|error): variable '(.*)' is uninitialized when used here", lines[0])
    if matches:
        response = [
            "It looks like you're trying to use the variable `{}` on line {} of `{}`.".format(matches.group(3), matches.group(2), matches.group(1)),
            "However, on that line, the variable `{}` doesn't have a value yet.".format(matches.group(3)),
            "Be sure to assign a value to `{}` before trying to access its value.".format(matches.group(3))
        ]
        if len(lines) >= 2 and re.search(matches.group(3), lines[1]):
            return (2, response)
        return (1, response)
