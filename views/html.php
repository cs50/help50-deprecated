<!DOCTYPE html>

<html lang="en">
    <head>

        <!-- http://getbootstrap.com/ -->
        <link href="css/bootstrap.min.css" rel="stylesheet"/>

        <!-- http://sourcefoundry.org/hack/ -->
        <link href="css/hack-extended.min.css" rel="stylesheet"/>

        <meta name="viewport" content="width=device-width, initial-scale=1">

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
            <pre><?= join("<br/>", array_map("htmlspecialchars", $lines)); ?></pre>
            <pre><?= preg_replace("/`([^`]+)`/", "<strong>$1</strong>", htmlspecialchars($help)); ?></pre>
        </div>
    </body>
</html>
