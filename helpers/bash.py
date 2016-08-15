import re
def help(lines):

    # No such file or directory
    matches = re.search(r"^bash: (.+): No such file or directory", lines[0])
    if matches:
        after = [
            "Are you sure `{}` exists".format(matches.group(1)),
            "Did you misspell `{}`?".format(matches.group(1))
        ]
        return (lines[0:1], after)

    # Permission denied
    matches = re.search(r"^bash: (.+): Permission denied", lines[0])
    if matches:
        after = [
            "`{}` couldn't be executed.".format(matches.group(1)),
            "Did you remember to make `{}` \"executable\" with `chmod +x {}`?".format(matches.group(1), matches.group(1))
        ]
        if (re.search(r"\.pl$", matches.group(1), re.I)):
            after.append("Did you mean to execute `perl {}`?".format(matches.group(1)))
        elif (re.search(r"\.php$", matches.group(1), re.I)):
            after.append("Did you mean to execute `php {}`?".format(matches.group(1)))
        elif (re.search(r"\.rb$", matches.group(1), re.I)):
            after.append("Did you mean to execute `ruby {}`?".format(matches.group(1)))
        return (lines[0:1], after)
