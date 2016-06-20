<?php

    if (preg_match("/^bash: (.+): No such file or directory/", $line, $matches)) {
        "Are you sure `{$matches[1]}` exists?"
        "Did you misspell `{$matches[1]}`?"
    }

    if (preg_match("/^bash: (.+): Permission denied/", $line, $matches)) {
        "{$matches[1]} couldn't be executed."
        "Did you remember to make `{$matches[1]}` \"executable\" with `chmod +x {$matches[1]}`?"
        if (preg_match("/\.pl$/i", $matches[1])) {
            "Did you mean to execute `perl {$matches[1]}`?"
        }
        if (preg_match("/\.php$/i", $matches[1])) {
            "Did you mean to execute `php {$matches[1]}`?"
        }
        if (preg_match("/\.py$/i", $matches[1])) {
            "Did you mean to execute `python {$matches[1]}`?"
        }
        if (preg_match("/\.rb$/i", $matches[1])) {
            "Did you mean to execute `ruby {$matches[1]}`?"
        }
    }

?>
