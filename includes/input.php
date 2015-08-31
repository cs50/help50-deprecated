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

        <!-- http://www.jacklmoore.com/autosize/ -->
        <script src="js/autosize.min.js"></script>

        <script>

            jQuery(function($) {

                autosize($('textarea'));

                $('textarea').focus();
                
                $('form').submit(function(eventObject) {

                    // prevent form's submission
                    eventObject.preventDefault();

                    // validate input
                    if ($('textarea').val().trim() === '') {
                        $('textarea').removeClass('alert-danger alert-success').addClass('alert-warning');
                        return;
                    }

                    // POST input
                    $.ajax({
                        contentType: 'application/json',
                        data: JSON.stringify($('textarea').val().split(/\r?\n/)),
                        dataType: 'json',
                        error: function(jqXHR, textStatus, errorThrown) {
                            $('textarea').removeClass('alert-success alert-warning').addClass('alert-danger');
                        },
                        method: 'POST',
                        success: function(data, textStatus, jqXHR) {
                            $('textarea').removeClass('alert-danger alert-warning').addClass('alert-success');
                            
                        }
                    });
                });

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
            <form>
                <div class="form-group">
                    <textarea class="form-control" placeholder="paste a command's output here" rows="3"></textarea>
                </div>
                <button class="btn btn-default" type="submit">help50</button>
            </form>
        </div>
    </body>
</html>
