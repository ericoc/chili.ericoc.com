from flask import Flask, render_template


app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html.j2"), 404


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
