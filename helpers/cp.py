import re
def help(lines):

    # $ cp foo bar
    # cp: overwrite ‘bar’?
    #
    # $ cp foo baz/bar
    # cp: overwrite ‘baz/bar’?
    matches = re.search(r"^cp: overwrite ‘(.+)’\?", lines[0])
    if matches:

        # if "/" is present in destination path, then assume copying to a new directory
        new_dir = "/" in matches.group(1)
        interpretation = "You are copying a file to `{}`, but there is already a file ".format(matches.group(1))
        interpretation += "there " if new_dir else "in the current directory "
        interpretation += "with the same name."

        response = [interpretation]
        response.append("To copy the file, replacing the old version, type `y` and press return.")
        response.append("Typing `n` and pressing return will cancel copying.")
        return (lines[0:1], response)
