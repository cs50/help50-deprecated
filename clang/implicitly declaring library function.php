<?php

    if (preg_match("/implicitly declaring library function '([^']+)'/", $line, $matches) {
        $function = $matches[1];
        if ($function === "printf") {
            return "Did you forget to `#include <stdio.h>` (in which `printf` is declared) atop your file?";
        }
        else {
            return "Did you forget to `#include` the header file in which `{$matches[1]}` is declared atop your file?";
        }
    }
    else {
        return false;
    }

?>
