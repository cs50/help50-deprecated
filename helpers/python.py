import re

def help(lines):

    # check for recognized output
    # Traceback (most recent call last):
    if not re.search(r"^Traceback \(most recent call last\):$", lines[0]):
        return

    # iterate over lines ourselves
    for i, line in enumerate(lines):

        # $ ./tweets asdf
        # Traceback (most recent call last):
        #  File "./tweets", line 45, in <module>
        #    main()
        #  File "./tweets", line 19, in main
        #    tweets = helpers.get_user_timeline(screen_name, 50)
        #  File "/root/helpers.py", line 45, in get_user_timeline
        #    raise RuntimeError("API_KEY not set")
        # RuntimeError: API_KEY not set
        # ...
        # RuntimeError: API_SECRET not set
        matches = re.search(r"^RuntimeError: (API_KEY|API_SECRET) not set$", line)
        if matches:
            response = [
                "`{}`, an environment variable, doesn't appear to be set, at least not in this tab".format(matches.group(1)),
                "Odds are you need to run `export {}=value`, where `value` is `{}`'s intended value.".format(matches.group(1), matches.group(1))
            ]
            return (lines[i:i+1], response)

        # OSError: [Errno 98] Address already in use
        matches = re.search(r"^OSError: \[Errno 98\] Address already in use$", line)
        if matches:
            response = [
                "Another program is already listening on that port.",
                "Do you perhaps have this same command running in another tab?"
            ]
            return (lines[i:i+1], response)
