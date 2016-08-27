import re
def help(lines):
    
    # overwrite
    matches = re.search(r"^cp: overwrite ‘(.+)’\?", lines[0])
    if matches:
        after = [
            "You are copying a file to `{}`, but there is already a file with the same name there.".format(matches.group(1)),
            "To copy the file, replacing the old version, type `y` and press return.",
            "Typing `n` and pressing return will cancel copying."
        ]
        return (lines[0:1], after)
