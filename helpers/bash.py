import re
def help(lines):

    # command not found
    matches = re.search(r"^bash: (.+): command not found", lines[0])
    if matches:
        after = [
            "Are you sure `{}` exists?".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1)),
            "Did you mean to execute `./{}`?".format(matches.group(1))
        ]
        return (lines[0:1], after)

    # No such file or directory
    matches = re.search(r"^bash: (.+): No such file or directory", lines[0])
    if matches:
        after = [
            "Are you sure `{}` exists".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1))
        ]
        return (lines[0:1], after)

    # Permission denied
    matches = re.search(r"^bash: .*?(([^/]+)\.([^/.]+)): Permission denied", lines[0])
    if matches:
        after = [
            "`{}` couldn't be executed.".format(matches.group(1))
        ]
        if (matches.group(3) == "c"):
            after.append("Did you mean to execute `./{}`?".format(matches.group(2)))
        elif (matches.group(3) == "pl"):
            after.append("Did you mean to execute `perl {}`?".format(matches.group(1)))
        elif (matches.group(3) == "php"):
            after.append("Did you mean to execute `php {}`?".format(matches.group(1)))
        elif (matches.group(3) == "rb"):
            after.append("Did you mean to execute `ruby {}`?".format(matches.group(1)))
        else:
            after.append("Did you remember to make `{}` \"executable\" with `chmod +x {}`?".format(matches.group(1), matches.group(1)))
        return (lines[0:1], after)
    
    # Remove file
    matches = re.search(r"^rm: remove regular (?:empty )?file ‘(.+)’\?", lines[0])
    if matches:
        empty = re.search(r"^rm: remove regular empty file", lines[0])
        after = [
            "The command you typed will remove the file `{}`.".format(matches.group(1))
        ]
        if empty:
            after.append("`{}` is an empty file.".format(matches.group(1)))
        after.append("If you wish to remove `{}`, type `y` and press return.".format(matches.group(1)))
        after.append("Typing `n` and pressing return will cancel the operation.")
        return (lines[0:1], after)
    
    # mv overwrite
    matches = re.search(r"^mv: overwrite ‘(.+)’\?", lines[0])
    if matches:
        after = [
            "You are moving a file to `{}`, but there is already a file with the same name there.".format(matches.group(1)),
            "To continue with the move operation and replace the old file, type `y` and press return.",
            "Typing `n` and pressing return will cancel the operation."
        ]
        return (lines[0:1], after)
    
    # cp overwrite
    matches = re.search(r"^cp: overwrite ‘(.+)’\?", lines[0])
    if matches:
        after = [
            "You are copying a file to `{}`, but there is already a file with the same name there.".format(matches.group(1)),
            "To continue with the copy operation and replace the old file, type `y` and press return.",
            "Typing `n` and pressing return will cancel the operation."
        ]
        return (lines[0:1], after)
