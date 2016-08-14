<?php

    if (preg_match("/^([^:]+):(\d+):(\d+): warning: extra tokens at end of #include directive/", $lines[0], $matches)) {
        print("You seem to have an error in `{$matches[1]}` on line {$matches[2]} at character {$matches[3]}.\n");
        print("By \"extra tokens\", `clang` means that you have one or more extra characters on that line that you shouldn't.\n");
        if (preg_match("/^\s*\^/", $lines[2])) {
            $token = substr($lines[1], strpos($lines[2], "^"));
            if ($token === ";") {
                print("Try removing the semicolon at the end of that line.\n");
            }
            else {
                print("Try removing the `{$token}` at the end of that line.");
            }
            return 3;
        }
        return 1;
    }

?>
