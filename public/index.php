<?php

    require(__DIR__ . "/vendor/autoload.php");

    if ($_SERVER["REQUEST_METHOD"] === "GET") {
        require("../includes/input.php");
    }
    else if ($_SERVER["REQUEST_METHOD"] === "POST") {
        require("../includes/upload.php");
    }
    else {
        http_response_code(501);
    }

?>
