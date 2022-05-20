import secrets
import string
from datetime import date, datetime
from time import sleep

import requests
from flask import Flask, jsonify, render_template, request, session, url_for

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app.config["SECRET_KEY"] = "change-me"


ALPHABET = string.ascii_letters + string.digits + string.punctuation
CAPTCHA_LEN = 8


@app.get("/")
def index():
    title, msg = "Home", "Welcome to our site.."
    return render_template(main_template(), msg=msg, title=title)


@app.get("/about_us")
def about():
    title, msg = "About Us", "All about us.."
    return render_template(main_template(), msg=msg, title=title)


@app.get("/gen_captcha")
def captcha_gen():
    captcha = "".join(secrets.choice(ALPHABET) for _ in range(CAPTCHA_LEN))
    session["captcha"] = captcha
    return jsonify({"captcha": captcha})


@app.route("/contact_us", methods=["GET", "POST"])
def contact():
    title, msg = "Contact Us", "Please contact us.."
    error = ""
    if request.method == "POST":
        user_captcha = request.form.get("captcha", "")
        captcha_challenge = session.pop("captcha", "")

        if user_captcha == captcha_challenge:
            name = request.form["name"]
            msg = f"Thank you for your message '{name}'. We'll be in touch with you shortly.."
            return render_template(main_template(), msg=msg, title=title)
        else:
            error = "Invalid captcha!"

    return render_template(
        main_template(),
        subtemplate_name="contact.html",
        msg=msg,
        error=error,
        title=title,
    )


@app.get("/clock")
def clock():
    if request.headers.get("Referer", "") == url_for("clock", _external=True):
        polls = int(session["polls"])
        if polls < 3:
            now = datetime.now().isoformat()
            msg = f"Current time is: {now}"
            status = 200
        else:
            msg = "OK, that's enough for now."
            status = 286

        session["polls"] = polls + 1
        return f"<li>{msg}</li>", status
    else:
        session["polls"] = "0"
        title, msg = "Clock", "Watch the time go by.."
        return render_template(
            main_template(), subtemplate_name="clock.html", msg=msg, title=title
        )


@app.get("/news_live")
def news():
    title, msg = "Breaking News", "Breaking news powered by SSE.."
    return render_template(
        main_template(), subtemplate_name="news.html", msg=msg, title=title
    )


@app.get("/event_source")
def event_source():
    def gen():
        import sys

        max_ = 3
        for i in range(max_):
            print("---", file=sys.stderr)
            now = datetime.now().isoformat()
            print(f"{i=} ({now=})", file=sys.stderr)
            print("---", file=sys.stderr)
            resp = "event: NewsAlert\n"
            resp += f"data: <span id='breaking-news'>Breaking news at: {now}</span>\n\n"
            yield resp

            if i < max_ - 1:
                sleep(2)

    return app.response_class(gen(), content_type="text/event-stream")


@app.get("/slow")
def slow():
    title, msg = "Slow Page", "Well.. that took a while..."
    sleep(3)
    return render_template(main_template(), msg=msg, title=title)


@app.get("/random_dog")
def random_dog():
    r = requests.get("https://dog.ceo/api/breeds/image/random")
    return jsonify(r.json())


@app.get("/client")
def client():
    title, msg = (
        "Powerful client-side Templates",
        "A quick taste of client-side templates..",
    )
    return render_template(
        main_template(), subtemplate_name="client.html", msg=msg, title=title
    )


def is_hx_req():
    return request.headers.get("HX-Request", "false") == "true"


def main_template():
    return "partial.html" if is_hx_req() else "index.html"


@app.context_processor
def inject_global_template_vars():
    return {"current_year": date.today().year}
