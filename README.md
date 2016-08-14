# CS50 Help

# Usage

## Command Line

_Coming Soon_

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

* Implement helper as a `.php` file in `includes/foo`, where `foo` is the name of the command for which the helper provides help
* Assume that `$lines` is in scope
* If helper recognizes `$lines[0]`
    * Print (to `stdout`) any advice
    * Return the number of lines recognized
* Else
    * Do not print anything
    * Do not return an `int`

# TODO

* Tidy code
* Tidy documentation
* Implement command-line client
* Simplify clang's output in IDE, as with some tweaks to:
    -fshow-column, -fshow-source-location, -fcaret-diagnostics, -fdiagnostics-fixit-info,  -fdiagnostics-parseable-fixits,
           -fdiagnostics-print-source-range-info, -fprint-source-range-info, -fdiagnostics-show-option, -fmessage-length
* Check how many hearts are standard to have. And whether half-hearts are always a thing.
* Steps?
    1. POST to /upload with cmd=&script=&username=. Get back { id: String }.
    1. GET /UUID.{ansi,html,json}?username=.
* Table:
    {
        "cmd": String,
        "created": Date,
        "description": "implicit declaration of function 'GetString'",
        "error": String,
        "hearts": Number,
        "id": Number,
        "module": "clang",
        "output": String, // TODO: decide on HTML or ANSI or troff or such; should include subset of input, so that parsing of CR and LF is all server-side; include mention of hearts; have usage come from server
        "script": String,
        "type": String, // JSON, ANSI, HTML
        "uuid": UUID4,
        "username": String,
        "version": String
    }
* Tables
    * inputs [GOOD, DONE]
        * id
        * uuid
        * cmd
        * script
        * username
    * hearts
        * id
        * username
        * hearts
        * lastmod
    * matches
        * id
        * input_id
        * match
* Input:
    cmd=&output=&script=&username=
* POST / output:
    {
        "id": UUID4,
        "hearts": Number
    }
* GET /UUID output:
    HTML or ANSI or Markdown
