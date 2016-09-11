import re
def help(lines):
    
    # $ ./a.out
    # Floating point exception
    matches = re.match("Floating point exception", lines[0])
    if matches:
        response = [
            "Looks like somewhere in your program, you're trying to divide a number by 0.",
            "Check to see where in your program you're using the `/` or `%` operators, and be sure you never divide by 0 or calculate a number modulo 0.",
            "If still unsure of where the problem is, stepping through your code with `debug50` may be helpful!"
        ]
        return (1, response)
    
    # $ ./a.out
    # Segmentation fault
    matches = re.match("Segmentation fault", lines[0])
    if matches:
        response = [
            "Looks like your program is trying to access areas of memory that it isn't supposed to access.",
            "There are many causes for segmentation faults, but you may want to consider:",
            "Are you trying to access an element of an array beyond the size of the array?",
            "Are you taking care to only dereference a pointer after you've initialized it (perhaps with `malloc`)?",
            "Have you checked that any pointers you're dereferencing aren't NULL?",
            "Are you trying to dereference a pointer after you've freed it?"
        ]
        return (1, response)