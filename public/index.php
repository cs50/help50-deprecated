<?php

    // GET /
    if ($_SERVER["REQUEST_METHOD"] === "GET") {
        render("index");
    }

    // POST /
    else if ($_SERVER["REQUEST_METHOD"] === "POST") {

        // check for script
        if (empty($_POST["script"])) {
            http_response_code(400);
            exit;
        }

        // split script into lines
        $lines = preg_split("/\r\n|\n|\r/", $_POST["script"], -1, PREG_SPLIT_NO_EMPTY);

        // check for format
        if (empty($_POST["format"]) || !in_array($_POST["format"], ["ansi", "html"])) {
            http_response_code(400);
            exit;
        }
        $format = $_POST["format"];

        // helpers to helper
        $helpers = array_filter(glob(__DIR__ . "/../includes/*/*.php"), "is_file");

        // iterate over lines
        for ($i = 0, $n = count($lines); $i < $n; $i++) {

            // iterate over helpers
            foreach ($helpers as $helper) {

                // try to help student with line $i onward
                $help = help($helper, array_slice($lines, $i), $matches);

                // if helpful
                if ($help !== false) {
                    if ($format === "ansi") {
                        render("ansi", ["lines" => $matches, "help" => $help]); // TODO: shouldn't render as HTML
                    }
                    else if ($format === "html") {
                        render("html", ["lines" => $matches, "help" => $help]);
                    }
                }
            }
        }

        // TODO
        echo "Sorry, can't help!";
        exit;
    }

    // Not Implemented
    http_response_code(501);
    exit;

    /**
     *
     */
    function help($helper, $lines, &$matches) {

        // get helper's contents
        $contents = file_get_contents($helper);

        // evaluate helper
        ob_start();
        $length = eval("?>" . $contents);
        $contents = trim(ob_get_contents());
        ob_end_clean();

        // return any help
        if (strlen($contents) > 0) {
            $matches = array_slice($lines, 0, $length);
            return $contents;
        }
        return false;
    }

    /**
     * Renders a template.
     */
    function render($view, $data = []) {
        extract($data);
        require(__DIR__ . "/../views/header.php");
        require(__DIR__ . "/../views/{$view}.php");
        require(__DIR__ . "/../views/footer.php");
        exit;
    }

?>
