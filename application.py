from flask import abort, Flask, render_template, request
import helpers
import model
import re

# application
app = Flask(__name__)

# preserve trailing newlines in templates (for format=ans and format=txt)
app.jinja_env.keep_trailing_newline = True

# configures database
@app.before_first_request
def configure():
    model.configure()

# /
@app.route("/", methods=["GET", "POST"])
def index():

    # POST
    if request.method == "POST":

        # validate format
        format = request.form.get("format")
        if format not in ["ans", "html", "txt"]:
            abort(400)

        # validate script
        script = request.form.get("script")
        if script is None:
            abort(400)

        # iteratively ask helpers for help with lines[i:]
        lines = script.splitlines()
        for i in iter(range(len(lines))):

            # iterate over helpers
            for helper in helpers.__all__:

                # ask helper for help
                help = helpers.__dict__.get(helper).help(lines[i:])

                # helpful response
                if help:
                    
                    # insert into db
                    cmd = helper
                    inputstring = "\n".join(help[0])
                    outputstring = "\n".join(help[1])
                    model.insert_input(cmd, inputstring)
                    model.insert_output(outputstring)
                    return render_template("helpful." + format, before=inputstring, after=outputstring)
                

        # unhelpful response
        # send only inputs to DB
        cmd = None 
        inputstring = script
        model.insert_input(cmd, inputstring)
        return render_template("unhelpful." + format, before="\n".join(lines))

    # GET, HEAD, OPTION
    else:
        return render_template("index.html")

# 400 Bad Request
@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400

# ANSI filter
@app.template_filter("ans")
def ans(value):
    return value

# HTML filter
@app.template_filter("html")
def html(value):
    return re.sub(r"`([^`]*)`", r"<strong>\1</strong>", value)
