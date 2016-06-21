<?php

    if (preg_match("/^([^:]+):(\d+):(\d+): warning: implicit declaration of function '([^']+)' is invalid/", $line, $matches)) {
        print("You seem to have an error in `{$matches[1]}` on line {$matches[2]} at character {$matches[3]}.\n");
        printf("By \"implicit declaration\", `clang` means that...\n");

        // TODO: finish porting below to this particular error
        if (preg_match("/^\s*^/", $lines[$i+2])) {
            // return $i through $i+2
            $token = substr($lines[$i+1], 19);
            if ($token === ";") {
                print("Try removing the semicolon at the end of that line.\n");
            }
            else {
                print("Try removing the `{$token}` at the end of that line.");
            }
        }
        // return $i
    }
    else {
        return false;
    }

?>
