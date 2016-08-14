<?php

    if (preg_match("/^([^:]+):(\d+):(\d+): warning: implicit declaration of function '([^']+)' is invalid/", $lines[0], $matches)) {
        print("You seem to have an error in `{$matches[1]}` on line {$matches[2]} at character {$matches[3]}.\n");
        printf("By \"implicit declaration\", `clang` means that...\n");
        // TODO
        return 1;
    }

?>
