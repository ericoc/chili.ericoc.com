from flask import Flask, flash, render_template, request
from flask_mail import Mail, Message


app = Flask(__name__)
app.config.from_pyfile("config.py")
mail = Mail(app)


@app.context_processor
def context():
    return {
        "SUBJECT": app.config["MAIL_SUBJECT"],
        "RECIPIENT": app.config["MAIL_RECIPIENT"]
    }


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html.j2")


@app.route("/", methods=["POST"])
def message():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    if not email and not phone:
        flash(
            message="Sorry, but please provide either an e-mail address or"
                    " telephone number where you can be contacted about Chili!",
            category="danger"
        )
        return index()

    with mail.connect() as conn:
        conn.send(
            Message(
                subject=app.config["MAIL_SUBJECT"],
                sender=app.config["MAIL_DEFAULT_SENDER"],
                body=f"Chili interest submission: {name} - {email} / {phone}",
                recipients=app.config["MAIL_RECIPIENT"],
            )
        )
        flash(
            category="success",
            message="Thank you - we will reach out to you about Chili soon!"
        )

    return index()


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html.j2"), 404


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
    mail.init_app(app)
