import re
from collections import namedtuple

def help(lines):

    # check for valgrind's output
    if not re.search(r"^==\d+== Memcheck, a memory error detector$", lines[0]):
        return

    # iterate over lines
    for i, line in enumerate(lines):

        # use of uninitialized value of size 8
        matches = re.search(r"^==\d+== Use of uninitialised value of size (\d+)$", line)
        if matches:
            response = [
                "Looks like you're trying to use a {}-byte variable that might not have a value?".format(matches.group(1)),
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                if issue.line:
                    response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
                else:
                    response.append("Take a closer look at `{}`.".format(issue.function))
                    response.append("And be sure to compile your program with `-ggdb3` to see line numbers in `valgrind`'s output.")
            return (lines[i:i+1], response)

        # invalid write of size 4
        matches = re.search(r"^==\d+== Invalid write of size (\d+)$", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like you're trying to store {} {} at a location in memory that you're not allowed to access?".format(matches.group(1), bytes),
                "Did you try to store something beyond the bounds of an array?"
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                if issue.line:
                    response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
                else:
                    response.append("Take a closer look at `{}`.".format(issue.function))
                    response.append("And be sure to compile your program with `-ggdb3` to see line numbers in `valgrind`'s output.")
            return (lines[i:i+1], response)

        # 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
        matches = re.search(r"^==\d+== (\d+) bytes in (\d+) blocks are definitely lost in loss record (\d+) of (\d+)$", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like your program leaked {} {} of memory.".format(matches.group(1), bytes),
                "Did you forget to `free` memory that you allocated via `malloc`?"
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                if issue.line:
                    response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
                else:
                    response.append("Take a closer look at `{}`.".format(issue.function))
                    response.append("And be sure to compile your program with `-ggdb3` to see line numbers in `valgrind`'s output.")
            return (lines[i:i+1], response)


    # iterate over lines again (for less precise errors)
    for i, line in enumerate(lines):

        # Conditional jump or move depends on uninitialised value(s)
        matches = re.search(r"^==\d+== Conditional jump or move depends on uninitialised value\(s\)$", line)
        if matches:
            response = [
                "Looks like you're trying to use a variable that might not have a value?",
            ]
            issue = issue_locate(lines[i+1:])
            if issue:
                if issue.line:
                    response.append("Take a closer look at line {} of `{}`.".format(issue.line, issue.file))
                else:
                    response.append("Take a closer look at `{}`.".format(issue.function))
                    response.append("And be sure to compile your program with `-ggdb3` to see line numbers in `valgrind`'s output.")
            return (lines[i:i+1], response)

        # definitely lost: 4 bytes in 1 blocks
        matches = re.search(r"^==\d+==    definitely lost: (\d+) bytes in (\d+) blocks$", line)
        if matches:
            bytes = "bytes" if int(matches.group(1)) > 1 else "byte"
            response = [
                "Looks like your program leaked {} {} of memory.".format(matches.group(1), bytes),
                "Did you forget to `free` memory that you allocated via `malloc`?"
            ]
            matches = re.search(r"^==\d+== Command: ([^\n]+)$.+^==\d+== Rerun with --leak-check=full to see details of leaked memory$", "\n".join(lines), re.DOTALL | re.MULTILINE)
            if matches:
                response.append("Run `valgrind --leak-check=full {}` for more details.".format(matches.group(1)))
            return (lines[i:i+1], response)

# finds the function, file, and line of an issue
def issue_locate(lines):

    # identify possible locations of issue
    locations = []
    Location = namedtuple('Location', 'address function file line')
    for line in lines:
        matches = re.search(r"^==\d+==    (?:at|by) (0x[0-9A-Fa-f]+): (.+) \((.+?)(?::(\d+))?\)", line)
        if matches:
            locations.append(Location(matches.group(1), matches.group(2), matches.group(3), matches.group(4)))
        else:
            break

    # infer actual location of issue
    locations.reverse()
    for i in range(len(locations)-1):

        # at 0x4C2AB80: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        # by 0x400546: foo (foo.c:6)
        # by 0x400568: main (foo.c:12)
        if (locations[i].line and not locations[i+1].line):
            return locations[i]

        # at 0x4C2AB80: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
        # by 0x400546: foo (in /srv/www/foo)
        # by 0x400568: main (in /srv/www/foo)
        if (not locations[i].line and locations[i].file != locations[i+1].file):
            return locations[i]

        # at 0x508299B: _itoa_word (_itoa.c:179)
        # by 0x5086636: vfprintf (vfprintf.c:1660)
        # by 0x5087E70: buffered_vfprintf (vfprintf.c:2356)
        # by 0x5082DFD: vfprintf (vfprintf.c:1313)
        # by 0x508D3D8: printf (printf.c:33)
        # by 0x40054C: main (foo.c:6)
        if (locations[i].line and locations[i+1].line and len(locations[i].address) < len(locations[i+1].address)):
            return locations[i]

    # at 0x40054F: foo (foo.c:7)
    # by 0x400568: main (foo.c:12)
    return locations[len(locations)-1] if locations else None
