<?php

    if (preg_match("/^bash: (.+): Permission denied/", $lines[0], $matches)) {
        print("{$matches[1]} couldn't be executed\n.");
        print("Did you remember to make `{$matches[1]}` \"executable\" with `chmod +x {$matches[1]}`?");
        if (preg_match("/\.pl$/i", $matches[1])) {
            print("Did you mean to execute `perl {$matches[1]}`?");
        }
        if (preg_match("/\.php$/i", $matches[1])) {
            print("Did you mean to execute `php {$matches[1]}`?");
        }
        if (preg_match("/\.py$/i", $matches[1])) {
            print("Did you mean to execute `python {$matches[1]}`?\n");
        }
        if (preg_match("/\.rb$/i", $matches[1])) {
            print("Did you mean to execute `ruby {$matches[1]}`?\n");
        }
        return 1;
    }

?>
