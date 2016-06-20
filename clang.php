<?php

    if (preg_match("/warning: implicitly declaring library function '([^']+)'/", $line, $matches)) {
        $function = $matches[1];
        if ($function === "printf") {
            "Did you forget to `#include <stdio.h>` (in which `printf` is declared) atop your file?"
        }
        else {
            "Did you forget to `#include` the header file in which `{$matches[1]}` is declared atop your file?"
        }
    }

    if (preg_match("/undefined reference to `([^']+)'/", $line, $matches)) {
        $function = $matches[1];
        if (preg_match("/^(get_char|get_double|get_float|get_int|get_long_long|get_string)$/", $function, $matches)) {
            "Did you forget to compile with `-lcs50` (in order to link against against the CS50 Library)?"
        }
        if (preg_match("/^(GetChar|GetDouble|GetFloat|GetInt|GetLongLong|GetString)$/", $function, $matches)) {
            "Did you forget to compile with `-lcs50` (in order to link against against the CS50 Library)?"
        }
        else if ($function === "crypt") {
            "Did you forget to compile with -lcrypt?"
        }
        else {
            $help["$i"] = "Did you forget to compile with `-lfoo`, where `foo` is the library that defines `{$function}`?";
        }
    }

    if (preg_match("/warning: extra tokens at end of #include directive/", $line, $matches)) {
        
    }

?>
