from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        format = request.form.get("format")
        return format
    else:
        return render_template("index.html")

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400
