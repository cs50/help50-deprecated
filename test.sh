#!/usr/bin/env php
<?php

    /*
    echo "\033[0;37m";
    echo "bash: ./foo: Permission denied\n";
    echo "\033[39m";
    echo "Did you remember to make test.php \"executable\" with `chmod +x {$matches[1]}`?\n";
    echo "\n";

    echo "\033[0;33m";
    echo "bash: ./foo: Permission denied\n";
    echo "\033[39m";
    echo "Did you remember to make test.php \"executable\" with `chmod +x {$matches[1]}`?\n";
    echo "\n";
    */

    /*
    echo "\033[0;37m";
    echo "1.c:1:19: warning: extra tokens at end of #include directive [-Wextra-tokens]\n";
    echo "#include <stdio.h>;\n";
    echo "                  ^\n";
    echo "                  //\n";
    echo "1 warning generated.\n";
    echo "\033[39m";
    */

    echo "\033[0;37m";
    echo "2.c:5:15: warning: implicit declaration of function 'GetString' is invalid in C99 [-Wimplicit-function-declaration]\n";
    echo "    char *s = GetString();\n";
    echo "              ^\n";
    echo "\033[39m";
    echo "\033[33m";
    echo "You seem to have an error in 2.c on line 5 at character 15.\n";
    echo "Did you forget to \033[1m#include <stdio.h>\033[0m\033[33m (in which `printf` is declared) atop your file?\n";
    echo "\033[39m";

    /*
    echo "\033[0;37m";
    echo "2.c:5:11: warning: incompatible integer to pointer conversion initializing 'char *' with an expression of type 'int' [-Wint-conversion]\n";
    echo "    char *s = GetString();\n";
    echo "          ^   ~~~~~~~~~~~\n";
    echo "2 warnings generated.\n";
    echo "Undefined symbols for architecture x86_64:\n";
    echo "  \"_GetString\", referenced from:\n";
    echo "      _main in 2-266656.o\n";
    echo "ld: symbol(s) not found for architecture x86_64\n";
    echo "clang: error: linker command failed with exit code 1 (use -v to see invocation)\n";
    echo "make: *** [2] Error 1\n";
    echo "\033[39m";
    */

?>
