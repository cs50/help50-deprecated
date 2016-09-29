import re

def help(lines):

    # $ ls asdf
    # ls: cannot access asdf: No such file or directory
    matches = re.search(r"^ls: cannot access (.+): No such file or directory", lines[0])
    if matches:
        response = [
            "Are you sure `{}` exists?".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1))
        ]
        return (lines[0:1], response)
