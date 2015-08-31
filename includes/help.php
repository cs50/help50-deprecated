<?php

    $lines = json_decode(file_get_contents("php://input"), true);

    $help = [];
    for ($i = 0, $n = count($lines); $i < $n; $i++) {
        $line = $lines[$i];

        if (preg_match("/warning: implicitly declaring library function '([^']+)'/", $line, $matches)) {
            if ($matches[1] === "printf") {
                $help["$i"] = "Did you forget to put `#include <stdio.h>` atop your file on a line of its own without a semicolon? Recall that `printf` is \"declared\" in `stdio.h`. Without that declaration, the compiler won't know what `printf` is.";
            }
            else {
                $help["$i"] = "Did you forget to `#include` the header file for `{$matches[1]}` atop your file?";
            }
        }

        if (preg_match("/undefined reference to `([^']+)'/", $line, $matches)) {
            $function = $matches[1];
            if (preg_match("/^(Get.+)$/", $function, $matches)) {
                $help["$i"] = "Did you forget to compile with -lcs50, which tells the compiler to \"link\" against the CS50 Library (i.e., combine its 0s and 1s with yours)?";
            }
            else if ($function === "crypt") {
                $help["$i"] = "Did you forget to compile with -lcrypt, which tells the compiler to \"link\" against the crypto library (i.e., combine its 0s and 1s with yours)?";
            }
            else {
                $help["$i"] = "Did you forget to link, as with -l, against whatever library implements {$function}?";
            }
        }
    }

    header("Content-type: application/json");
    print(json_encode((object) $help));

?>
