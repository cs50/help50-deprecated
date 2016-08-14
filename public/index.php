<?php

    function ansi($lines, $help) {
        render("ansi", ["lines" => $lines, "help" => $help]);
    }

    function help($pattern, $lines, &$matches) {
        $contents = file_get_contents($pattern);
        ob_start();
        $length = eval("?>" . $contents);
        $contents = trim(ob_get_contents());
        ob_end_clean();
        if (strlen($contents) > 0) {
            $matches = array_slice($lines, 0, $length);
            return $contents;
        }
        return false;
    }

    function render($view, $data = []) {
        extract($data);
        require(__DIR__ . "/../views/header.php");
        require(__DIR__ . "/../views/{$view}.php");
        require(__DIR__ . "/../views/footer.php");
        exit;
    }

    function html($lines, $help) {
        render("html", ["lines" => $lines, "help" => $help]);
    }

    if ($_SERVER["REQUEST_METHOD"] === "GET") {
        render("index");
    }
    else if ($_SERVER["REQUEST_METHOD"] === "POST") {

        // check for script
        if (empty($_POST["script"])) {
            http_response_code(400);
            exit;
        }

        // split script into lines
        $lines = preg_split("/\r\n|\n|\r/", $_POST["script"], -1, PREG_SPLIT_NO_EMPTY);

        // check for output's format
        if (empty($_POST["output"]) || !in_array($_POST["output"], ["ansi", "html"])) {
            http_response_code(400);
            exit;
        }
        $output = $_POST["output"];

        // helpers to include
        $includes = array_filter(glob(__DIR__ . "/../includes/*/*.php"), "is_file");

        // iterate over lines
        for ($i = 0, $n = count($lines); $i < $n; $i++) {

            // iterate over helpers
            foreach ($includes as $include) {

                // try to help student with line $i onward
                $help = help($include, array_slice($lines, $i), $matches);

                // if helpful
                if ($help !== false) {
                    if ($output === "ansi") {
                        ansi($matches, $help);
                    }
                    else if ($output === "html") {
                        html($matches, $help);
                    }
                }
            }
        }
    }
    else {
        http_response_code(501);
        exit;
    }

?>
