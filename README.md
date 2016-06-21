# help50

# TODO

* Look up how to do PHP HEREDOCs.
* Port server to node.js so as to implement as modules?
* Treat $lines as a stream with a cursor so that any matches consume 1+ lines from stream and advance cursor? Or delete lines from array.
* Ensure clang.php and such can consume unnecessary lines, so that helpful messages can go underneath. E.g.:
    1.c:1:19: warning: extra tokens at end of #include directive [-Wextra-tokens]
    #include <stdio.h>;
                      ^
                      //
    1 warning generated.
* Simplify clang's output in IDE, as with some tweaks to:
    -fshow-column, -fshow-source-location, -fcaret-diagnostics, -fdiagnostics-fixit-info,  -fdiagnostics-parseable-fixits,
           -fdiagnostics-print-source-range-info, -fprint-source-range-info, -fdiagnostics-show-option, -fmessage-length
* Ask Dan A if we can generate a unique ID per workspace with a particular checksum. Or how to get C9 username. Or sid from OAuth2.
* Check if in JS an array can have gaps in arrays, so that server can return a sparse array, each of whose indexes represents help for that line of input.
* Possible to convert HTML to ANSI, so that server can just return a formatted response?
* Check how many hearts are standard to have. And whether half-hearts are always a thing.
* Steps
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
