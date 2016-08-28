# Usage

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

## Command Line

Assuming a container is running and listening at `http://localhost:8080/` and you're inside of the container (via `docker exec -it help50_web bash -l`):

* `help50 ./foo`
* `help50 make foo`
* `help50 clang -o foo foo.c`
* `./foo |& help50`
* `make foo |& help50`
* `clang -o foo foo.c |& help50`

# Contributing

To contribute a sample error message that `help50` does yet support, [open an issue](https://github.com/cs50/help50/issues) and provide, ideally, both the error message and the command (and code, if any) that triggered it, both formatted in Markdown like [code](https://guides.github.com/features/mastering-markdown/#syntax).

Better yet, to contribute to a helper for `foo`, implement `helpers/foo.py` per the below, where `lines` will be an array of strings (i.e., lines of `stderr` and/or `stdout` potentially from `foo`) for which user needs help, `before` must be a slice of `lines` that this helper has matched on, and `after` must be an array of strings that help user understand `before`. Helper must return `None` if it does not recognize `lines[0]`. Only if helper recognizes `lines[0]` may it look at `lines[1:]`.

```python
import re
def help(lines):
    ...
    # if helper recognizes lines[0]
        ...
        return (before, after)
```

# TODO

* Get ANSI codes to work in server-side `.ans` templates.
* Decide whether server should return `before` for `.ans` (and `.txt`) templates.
* Replace backticks with ANSI boldfacing, a la https://github.com/cs50/help50/blob/php/malan/test.sh?
* When helpers fail to match first few lines of `script` (e.g., `examples/c/0.c`), don't just show the matched lines as `before`, show preceding lines too?
* Create `client` and `server` subdirectories? But Elastic Beanstalk might only look in root of repo.
* Add support for usernames and hearts via a MySQL database.
* Create tests (that get executed before deployment).
