import re
def help(lines):

    # $ $ foo
    # bash: foo: command not found
    matches = re.search(r"^bash: (.+): command not found", lines[0])
    if matches:
        after = [
            "Are you sure `{}` exists?".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1)),
            "Did you mean to execute `./{}`?".format(matches.group(1))
        ]
        return (1, after)

    # $ cd foo
    # bash: cd: foo: No such file or directory
    matches = re.search(r"^bash: (.+): No such file or directory", lines[0])
    if matches:
        after = [
            "Are you sure `{}` exists".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1))
        ]
        return (1, after)

    # $ ./foo
    # bash: ./foo: Permission denied
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
        return (1, after)
