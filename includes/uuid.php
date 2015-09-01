<?php

    try {

         // get text from S3
         $s3 = new Aws\S3\S3Client([
             "region"  => "us-east-1",
             "version" => "latest"
         ]);
         $result = $s3->getObject([
             "Bucket" => $_ENV["AWS_S3_BUCKET"],
             "Key" => $_SERVER["REQUEST_URI"]
         ]);
     }
     catch (UnsatisfiedDependencyException $e) {
         http_response_code(500);
         exit(0);
     }
     catch (S3Exception $e) {
         http_response_code(500);
         exit(0);
     }
     catch (AwsException $e) {
         http_response_code(500);
         exit(0);
     }

?>

<!DOCTYPE html>

<html lang="en">
    <head>

        <!-- http://getbootstrap.com/ -->
        <link href="css/bootstrap.min.css" rel="stylesheet"/>

        <!-- http://sourcefoundry.org/hack/ -->
        <link href="css/hack-extended.min.css" rel="stylesheet"/>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script src="js/jquery-1.11.3.min.js"></script>

        <script src="js/bootstrap.min.js"></script>

        <script>

            jQuery(function($) {
                // TODO
            });

        </script>

        <style>
            
            body {
                font-family: Hack, monospace;
                margin: 50px;
            }

        </style>

        <title>CS50 Help</title>

    </head>
    <body>
        <div class="container">
            TODO
        </div>
    </body>
</html>
