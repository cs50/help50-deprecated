import re
def help(lines):

    # $ $ foo
    # bash: foo: command not found
    matches = re.search(r"^bash: (.+): command not found", lines[0])
    if matches:
        response = [
            "Are you sure `{}` exists?".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1)),
            "Did you mean to execute `./{}`?".format(matches.group(1))
        ]
        return (1, response)

    # $ cd foo
    # bash: cd: foo: No such file or directory
    matches = re.search(r"^bash: cd: (.+): No such file or directory", lines[0])
    if matches:
        response = [
            "Are you sure `{}` exists?".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1))
        ]
        return (1, response)

    # $ cd foo
    # bash: cd: foo: Not a directory
    matches = re.search(r"^bash: cd: (.+): Not a directory", lines[0])
    if matches:
        response = [
            "Looks like you're trying to change directories, but `{}` isn't a directory.".format(matches.group(1)),
            "Did you mean to create the directory `{}` first?".format(matches.group(1))
        ]
        return (1, response)

    # $ ./foo
    # bash: ./foo: Permission denied
    matches = re.search(r"^bash: .*?(([^/]+)\.([^/.]+)): Permission denied", lines[0])
    if matches:
        response = [
            "`{}` couldn't be executed.".format(matches.group(1))
        ]
        if (matches.group(3) == "c"):
            response.append("Did you mean to execute `./{}`?".format(matches.group(2)))
        elif (matches.group(3) == "pl"):
            response.append("Did you mean to execute `perl {}`?".format(matches.group(1)))
        elif (matches.group(3) == "php"):
            response.append("Did you mean to execute `php {}`?".format(matches.group(1)))
        elif (matches.group(3) == "rb"):
            response.append("Did you mean to execute `ruby {}`?".format(matches.group(1)))
        else:
            response.append("Did you remember to make `{}` \"executable\" with `chmod +x {}`?".format(matches.group(1), matches.group(1)))
        return (1, response)
