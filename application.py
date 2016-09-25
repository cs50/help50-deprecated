from flask import abort, Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import flask_migrate
import helpers
import manage
import model
import os
import re

# application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://" + os.environ["MYSQL_USERNAME"] + ":" + os.environ["MYSQL_PASSWORD"] + "@" + os.environ["MYSQL_HOST"] + "/" + os.environ["MYSQL_DATABASE"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# preserve trailing newlines in templates (for format=ans and format=txt)
app.jinja_env.keep_trailing_newline = True

# perform any migrations
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
                    before, after = help
                    if (len(before) < len(lines[i:])):
                        before.append("...")
                    before = "\n".join(before)
                    after = " ".join(after)
                    model.log(request.form.get("cmd"), request.form.get("username"), request.form.get("script"), after)
                    return render_template("helpful." + format, before=before, after=after)

        # unhelpful response
        model.log(request.form.get("cmd"), request.form.get("username"), request.form.get("script"), None)
        return render_template("unhelpful." + format, before="\n".join(lines))

    # GET, HEAD, OPTION
    else:
        return render_template("index.html")

@app.route('/review', methods=["GET", "POST"])
def review():

    # POST if submitted password
    if request.method == "POST":
        # user submitted password to access review page
        if ("password" in request.form):
            if (request.form.get("password") == os.environ["HELP50_PASSWORD"]):
                return render_template("review.html", inputs=model.unreviewed_matchless())
            else:
                return render_template("review_auth.html", invalid=True)

        # user submitted form on review page
        else:
            for input_id in request.form:
                model.mark_reviewed(input_id)
            return render_template("review.html", inputs=model.unreviewed_matchless())

    # GET, show authorization page
    else:
        return render_template("review_auth.html")

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
