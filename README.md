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
