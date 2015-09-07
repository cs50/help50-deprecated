<?php

print "<PRE>"; print(getenv("AWS_S3_BUCKET")); exit;

    require(__DIR__ . "/../vendor/autoload.php");

    if ($_SERVER["REQUEST_METHOD"] === "GET") {
        require("../includes/get.php");
    }
    else if ($_SERVER["REQUEST_METHOD"] === "POST") {
        require("../includes/post.php");
    }
    else {
        http_response_code(501);
    }

?>
