import re

def help(lines):

    # check for recognized output
    # Traceback (most recent call last):
    if not re.search(r"^Traceback \(most recent call last\):$", lines[0]):
        return

    # iterate over lines ourselves
    for i, line in enumerate(lines):

        # OSError: [Errno 98] Address already in use
        matches = re.search(r"^OSError: \[Errno 98\] Address already in use$", line)
        if matches:
            response = [
                "Another program is already listening on that port.",
                " Do you perhaps have this same command running in another tab?"
            ]
            return (lines[i:i+1], response)
