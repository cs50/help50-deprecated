# help50

# TODO

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
* Ask Dan A if we can generate a unique ID per workspace with a particular checksum.
* Check if in JS an array can have gaps in arrays, so that server can return a sparse array, each of whose indexes represents help for that line of input.
* Possible to convert HTML to ANSI, so that server can just return a formatted response?
* Output format:
    {
        "cmd": String,
        "created": Date,
        "id": Number,
        "input": String,
        "match": "implicit declaration of function 'GetString'",
        "matcher": "clang",
        "output": String, // TODO: decide on HTML or ANSI or troff or such; should include subset of input, so that parsing of CR and LF is all server-side
        "uuid": UUID4,
        "username": String,
        "version": String
    }
