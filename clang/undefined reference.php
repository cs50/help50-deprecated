<?php

    if (preg_match("/undefined reference to `([^']+)'/", $line, $matches)) {
        print("By \"undefined reference,\" `clang` means that you've called a function, `{$matches[1]}`, that doesn't seem to be implemented. If that function has, in fact, been implemented, odds are you've forgotten to tell `clang` to \"link\" against the file that implements `{$matches[1]}`.\n");
        $function = $matches[1];
        if (preg_match("/^(get_char|get_double|get_float|get_int|get_long_long|get_string)$/", $function, $matches)) {
            print("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{$matches[1]}`?\n");
        }
        if (preg_match("/^(GetChar|GetDouble|GetFloat|GetInt|GetLongLong|GetString)$/", $function, $matches)) {
            print("Did you forget to compile with `-lcs50` in order to link against against the CS50 Library, which implements `{$matches[1]}`?\n");
        }
        else if ($function === "crypt") {
            print("Did you forget to compile with -lcrypt in order to link against the crypto library, which implemens `crypt`?\n");
        }
        else {
            print("Did you forget to compile with `-lfoo`, where `foo` is the library that defines `{$function}`?\n");
        }
    }
    else {
        return false;
    }

?>
