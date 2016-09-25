import re

def help(lines):

    # definitely lost: 4 bytes in 1 blocks
    matches = re.search(r"definitely lost: (\d+) bytes in (\d+) blocks", lines[0])
    if matches:
        response = [
            "Looks like your program leaked {} bytes worth of memory.".format(matches.group(1)),
            "Did you forget to `free` memory that you allocated using `malloc`?"
        ]
        return (lines[0:1], response)
