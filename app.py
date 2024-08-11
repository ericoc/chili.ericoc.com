from flask import Flask, flash, render_template


# Flask.
app = Flask(__name__)
app.config.from_pyfile("config.py")


def _error(
    message="Sorry, but there was an unknown error.",
    category="warn",
    code=500
):
    """Error handler."""
    flash(message, category)
    return render_template("index.html.j2"), code or 500


@app.errorhandler(404)
def _page_not_found(message):
    """Page Not Found (404 error handler)."""
    return _error(message=message, code=404)


@app.before_request
def start():
    """Start."""
    pass


@app.route("/", methods=["GET"])
def index():
    """Index."""
    return render_template("index.html.j2")


@app.teardown_appcontext
def end(err=None):
    """End."""
    if err:
        raise err


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
