from flask import Flask, flash, make_response, render_template, request
from flask_mail import Mail, Message
from wtforms import Form, EmailField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, Optional


class ContactForm(Form):
    name = StringField(label="name", validators=(DataRequired(),))
    email = EmailField(label="email", validators=(Email(), Optional()))
    phone = TelField(label="tel", validators=(Optional(),))
    submit = SubmitField(label="Submit")


app = Flask(__name__)
app.config.from_pyfile("config.py")
mail = Mail(app)


@app.context_processor
def context():
    return {
        "SUBJECT": app.config["MAIL_SUBJECT"],
        "RECIPIENT": app.config["MAIL_RECIPIENT"],
        "TELEPHONE": app.config["TELEPHONE"],
    }


@app.route("/", methods=["GET", "POST"])
def index():

    set_cookie = False
    form = ContactForm(request.form)
    if bool(request.cookies.get(app.config["COOKIE"], False)) is True:
        form = None

    if form is not None and form.validate():
        name = form.name.data or None
        email = form.email.data or None
        phone = form.phone.data or None

        if not email and not phone:
            flash(
                message=(
                    "Sorry, but please provide either an e-mail address or"
                    " telephone number where you can be contacted about Chili!"
                ),
                category="danger"
            )

        else:
            with mail.connect() as conn:
                conn.send(
                    Message(
                        subject=app.config["MAIL_SUBJECT"],
                        sender=app.config["MAIL_DEFAULT_SENDER"],
                        body=(
                            f'{app.config["MAIL_SUBJECT"]} interest submission:'
                            f"\n{name} - {email} / {phone}"
                        ),
                        recipients=[app.config["MAIL_RECIPIENT"]],
                    )
                )
                flash(
                    category="success",
                    message=(
                        "Thank you - we will reach out to you about Chili soon!"
                    )
                )
                form = None
                set_cookie = True

    resp = make_response(render_template("index.html.j2", form=form))
    if set_cookie is True:
        resp.set_cookie(key=app.config["COOKIE"], value=str(True))
    return resp


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html.j2"), 404


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
    mail.init_app(app)
