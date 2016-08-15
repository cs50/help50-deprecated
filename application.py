from flask import abort, Flask, render_template, request
import helpers

# application
app = Flask(__name__)

# /
@app.route("/", methods=["GET", "POST"])
def index():

    # POST
    if request.method == "POST":

        # validate format
        format = request.form.get("format")
        if format not in ["ans", "html"]:
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
                    return render_template("helpful." + format, before=help[0], after=help[1])

        # unhelpful response
        return render_template("unhelpful." + format, before="\n".join(lines))

    # GET, HEAD, OPTION
    else:
        return render_template("index.html")

# 400 Bad Request
@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400
