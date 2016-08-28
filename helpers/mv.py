import re
def help(lines):
   
    # $ mv foo bar
    # mv: overwrite ‘bar’?
    matches = re.search(r"^mv: overwrite ‘(.+)’\?", lines[0])
    if matches:
        after = [
            "You are moving a file to `{}`, but there is already a file with the same name there.".format(matches.group(1)),
            "To continue with the move operation and replace the old file, type `y` and press return.",
            "Typing `n` and pressing return will cancel the operation."
        ]
        return (lines[0:1], after)