<?php

    require(__DIR__ . "/../vendor/autoload.php");

    use Aws\Exception\AwsException;
    use Aws\S3\Exception\S3Exception;
    use Rhumsaa\Uuid\Uuid;
    use Rhumsaa\Uuid\Exception\UnsatisfiedDependencyException;

    // validate text
    if (empty($_POST["text"])) {
        http_response_code(400);
        exit(0);
    }

    // TODO: tidy error handling

    // upload text
    try {

        print "<PRE>"; print_r(getenv("AWS_S3_BUCKET")); exit;
        // generate UUID for text
        $uuid = Uuid::uuid4()->toString();

        // put text in S3
        $s3 = new Aws\S3\S3Client([
            "region"  => "us-east-1",
            "version" => "latest"
        ]);
        $s3->putObject([
            "Body" => $_POST["text"],
            "Bucket" => $_ENV["AWS_S3_BUCKET"],
            "Key" => $uuid
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
    catch (Exception $e) {
        print "<PRE>"; print_r($e); exit;
    }

    // TODO: detect AWS proxy
    $protocol = (isset($_SERVER["HTTPS"])) ? "https" : "http";
    $host = $_SERVER["HTTP_HOST"];
    header("Location: {$protocol}://{$host}/{$uuid}");
    
?>
