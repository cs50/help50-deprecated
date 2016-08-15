# Usage

## Command Line

* `bin/help50 ./foo`
* `help50 make foo`
* `bin/help50 clang -o foo foo.c`
* `./foo |& bin/help50`
* `make foo |& bin/help50`
* `clang -o foo foo.c |& bin/help50`

## Web

1. Install [Docker Engine](https://docs.docker.com/engine/installation/)
1. Execute `docker-compose build` in a terminal
1. Execute `docker-compose up` in a terminal
1. Visit `http://localhost:8080/` in a browser

The provided `docker-compose.yml` will "mount" the repository within the container (at `/srv/www`) so that you can make changes to files locally that will be reflected inside the container.

For a shell within the container, execute

```
docker exec -it help50_web bash -l
```

after the container has been started (with `docker-compose up`).

# Contributing

To contribute to a helper for `foo`, implement `helpers/foo.py` per the below, where `lines` will be an array of strings (i.e., lines of `stderr` and/or `stdout` potentially from `foo`) for which user needs help, `before` must be a slice of `lines` that this helper has matched on, and `after` must be an array of strings that help user understand `before`. Helper must return `None` if it does not recognize `lines[0]`. Only if helper recognizes `lines[0]` may it look at `lines[1:]`.

```python
import re
def help(lines):
    ...
    # if helper recognizes lines[0]
        ...
        return (before, after)
```

# TODO

* Add `username` to CLI.
* Add `https://help.cs50.net/` to CLI.
* Get ANSI codes to work in server-side `.ans` templates.
* Decide whether server should return `before` for `.ans` (and `.txt`) templates.
* Replace backticks with ANSI boldfacing, a la https://github.com/cs50/help50/blob/php/malan/test.sh?
* When helpers fail to match first few lines of `script` (e.g., `examples/c/0.c`), don't just show the matched lines as `before`, show preceding lines too?
* Create `client` and `server` subdirectories?
* Create examples in `examples` that test helpers.
* Add support for usernames and hearts via a MySQL database.

# Sample Inputs

```
bash: ./foo: No such file or directory
```

```
1.c:1:19: warning: extra tokens at end of #include directive [enabled by default]
 #include <stdio.h>;
                   ^
```

```
2.c: In function ‘main’:
2.c:5:15: warning: initialization makes pointer from integer without a cast [enabled by default]
     char *s = GetString();
               ^
/tmp/ccM1A4OG.o: In function `main':
2.c:(.text+0xe): undefined reference to `GetString'
collect2: error: ld returned 1 exit status
make: *** [2] Error 1
```

```
/tmp/ccOsNy8L.o: In function `main':
3.c:(.text+0xe): undefined reference to `GetString'
collect2: error: ld returned 1 exit status
make: *** [3] Error 1
```
