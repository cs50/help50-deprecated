<?php

    if (preg_match("/implicitly declaring library function '([^']+)'/", $lines[0], $matches)) {
        $function = $matches[1];
        if ($function === "printf") {
            print("Did you forget to `#include <stdio.h>` (in which `printf` is declared) atop your file?");
        }
        else {
            print("Did you forget to `#include` the header file in which `{$matches[1]}` is declared atop your file?");
        }
        return 1;
    }

?>
