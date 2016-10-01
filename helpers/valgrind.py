import re
from collections import namedtuple

def help(lines):

    # check for valgrind's output
    if not re.search(r"^==\d+== Memcheck, a memory error detector$", lines[0]):
        return

    # iterate over lines
    for i, line in enumerate(lines):

        # use of uninitialized value of size 8
        matches = re.search(r"Use of uninitialised value of size (\d+)", line)
        if matches:
            response = [
                "Looks like you're trying to access a variable that you might not have assigned a value?",
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
            return (lines[i:i+1], response)

        # invalid write of size 4
        matches = re.search(r"Invalid write of size (\d+)", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like you're trying to store {} {} at a location in memory that you're not allowed to access?".format(matches.group(1), bytes),
                "Did you try to store something beyond the bounds of an array?"
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
            return (lines[i:i+1], response)

        # 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
        matches = re.search(r"(\d+) bytes in (\d+) blocks are definitely lost in loss record (\d+) of (\d+)", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like your program leaked {} {} of memory.".format(matches.group(1), bytes),
                "Did you forget to `free` memory that you allocated using `malloc`?"
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
            return (lines[i:i+1], response)

        # definitely lost: 4 bytes in 1 blocks
        matches = re.search(r"definitely lost: (\d+) bytes in (\d+) blocks", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like your program leaked {} {} of memory.".format(matches.group(1), bytes),
                "Did you forget to `free` memory that you allocated using `malloc`?"
            ]
            matches = re.search(r"^==\d+== Command: ([^\n]+)$.+^==\d+== Rerun with --leak-check=full to see details of leaked memory$", "\n".join(lines), re.DOTALL | re.MULTILINE)
            if matches:
                response.append("Run `valgrind --leak-check=full {}` for more details.".format(matches.group(1)))
            return (lines[i:i+1], response)

# finds the function, file, and line of a valgrind error
def issue_locate(lines):
    locations = []
    Location = namedtuple('Location', 'function file line')
    search_next_line = True
    n = 0
    # iterate through lines of valgrind output
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
        print("\n".join(lines))
        return None

    # reverse the list and search for the most likely source of the error
    locations.reverse()
    previous_location = locations[0]
    for location in locations:
        if (location.file != previous_location[1]):
            return previous_location
        previous_location = location

    return previous_location
