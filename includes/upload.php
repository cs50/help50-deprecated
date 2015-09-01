<?php

    if (empty($_POST["text"])) {
        http_response_code(400);
        exit(0);
    }

    $s3 = new Aws\S3\S3Client([
        "region"  => "us-east-1",
        "version" => "latest"
    ]);

    $result = $s3->putObject([
        "Bucket" => "my-bucket",
        "Key" => "my-key",
        "Body" => $_POST["text"]
    ]);
]);   
?>
