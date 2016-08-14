<?php

    if (preg_match("/^bash: (.+): No such file or directory/", $lines[0], $matches)) {
        print("Are you sure `{$matches[1]}` exists?\n");
        print("Did you misspell `{$matches[1]}`?\n");
        return 1;
    }

?>
