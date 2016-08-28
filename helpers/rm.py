import re
def help(lines):
    
    # $ rm foo
    # rm: remove regular file ‘foo’?
    #
    # $ rm foo
    # rm: remove regular empty file ‘foo’?
    matches = re.search(r"^rm: remove regular (?:empty )?file ‘(.+)’\?", lines[0])
    if matches:
        empty = re.search(r"^rm: remove regular empty file", lines[0])
        after = [
            "The command you typed will delete the file `{}`".format(matches.group(1))
        ]
        after[0] += " (which is empty anyway)." if empty else "."
        after.append("If you wish to delete `{}`, type `y` and press return.".format(matches.group(1)))
        after.append("Typing `n` and pressing return will cancel the operation.")
        return (lines[0:1], after)