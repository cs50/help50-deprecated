import re
from collections import namedtuple

def help(lines):

    # definitely lost: 4 bytes in 1 blocks
    matches = re.search(r"definitely lost: (\d+) bytes in (\d+) blocks", lines[0])
    if matches:
        response = [
            "Looks like your program leaked {} bytes of memory.".format(matches.group(1)),
            "Did you forget to `free` memory that you allocated using `malloc`?"
        ]
        return (lines[0:1], response)

    # use of uninitialized value of size 8
    matches = re.search(r"Use of uninitialised value of size (\d+)", lines[0])
    if matches:
        response = [
            "Looks like you're trying to access a variable that you might not have assigned a value.",
        ]
        issue = issue_locate(lines[1:])
        if issue:
            response.append("Pay attention to line {} of `{}`.".format(issue.line, issue.file))
        return (lines[0:1], response)

    # invalid write of size 4
    matches = re.search(r"Invalid write of size (\d+)", lines[0])
    if matches:
        response = [
            "Looks like you tried to store {} bytes of data in memory you weren't allowed to access.".format(matches.group(1)),
            "Did you try to store data beyond the bounds of an array?"
        ]
        return (lines[0:1], response)


# finds the function, file, and line of a Valgrind error
def issue_locate(lines):
    locations = []
    Location = namedtuple('Location', 'function file line')
    search_next_line = True
    n = 0
    # iterate through lines of Valgrind output
    while (search_next_line and n < len(lines)):
        matches = re.search("(?:at|by) 0x.*: (.*) \((.*):(\d+)\)", lines[n])
        # if we found a function, add it to the list of possible locations
        if matches:
            n += 1
            locations.append(Location(matches.group(1), matches.group(2), matches.group(3)))
        # stop iterating once we've reached the end of function lines
        else:
            search_next_line = False

    if (len(locations) == 0):
        return None

    # reverse the list and search for the most likely source of the error
    locations.reverse()
    previous_location = locations[0]
    for location in locations:
        if (location.file != previous_location[1]):
            return previous_location
        previous_location = location

    return previous_location
