from flask import abort, Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import flask_migrate
import helpers
import manage
import os
import re

# application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# preserve trailing newlines in templates (for format=ans and format=txt)
app.jinja_env.keep_trailing_newline = True

@app.before_first_request
def configure():
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    flask_migrate.upgrade() 

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
                    return render_template("helpful." + format, before="\n".join(help[0]), after="\n".join(help[1]))

        # unhelpful response
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