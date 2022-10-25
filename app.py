import json
import re
import secrets
import string
from datetime import date, datetime
from time import sleep

import requests
from flask import Flask, jsonify, render_template, request, session, url_for
from flask_sock import Sock

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"
app.config["SECRET_KEY"] = "change-me"
app.config["CITIES"] = [
    "Buenos Aires",
    "Colonia del Sacramento",
    "Edinburgh",
    "Glasgow",
    "San Diego",
]
sock = Sock(app)


ALPHABET = string.ascii_letters + string.digits + string.punctuation
CAPTCHA_LEN = 8


@app.get("/")
def index():
    title, msg = "Home", "Welcome to our site.."
    return render_template(_main_template(), msg=msg, title=title)


@app.get("/about_us")
def about():
    title, msg = "About Us", "All about us.."
    return render_template(_main_template(), msg=msg, title=title)


@app.get("/gen_captcha")
def captcha_gen():
    captcha = "".join(secrets.choice(ALPHABET) for _ in range(CAPTCHA_LEN))
    session["captcha"] = captcha
    return jsonify({"captcha": captcha})


@app.get("/cities")
def cities():
    cities = app.config["CITIES"]
    if q := request.args.get("q"):
        regex = re.compile(q, re.I)
        cities = [city for city in cities if regex.search(city)]

    return jsonify({"cities": cities})


@app.route("/contact_us", methods=["GET", "POST"])
def contact():
    title, msg = "Contact Us", "Please contact us.."
    error = ""
    if request.method == "POST":
        user_captcha = request.form.get("captcha", "")
        captcha_challenge = session.pop("captcha", "")

        if user_captcha == captcha_challenge:
            name = request.form["name"]
            city = request.form["city"]
            pic = request.files["pic"]
            msg = (
                f"'{name}' from '{city}':  thank you for your lovely pic ({pic.filename})."
                " We'll be in touch with you shortly.."
            )
            return render_template(_main_template(), msg=msg, title=title)
        else:
            error = "Invalid captcha!"

    return render_template(
        _main_template(),
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
            now = datetime.now().replace(microsecond=0).isoformat()
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
            _main_template(), subtemplate_name="clock.html", msg=msg, title=title
        )


@app.get("/sse_news")
def sse_news():
    title, msg = "Breaking News", "Breaking news powered by SSE.."
    return render_template(
        _main_template(), subtemplate_name="sse.html", msg=msg, title=title
    )


@app.get("/event_source")
def event_source():
    def gen():
        max_ = 3
        for i in range(max_):
            now = datetime.now().replace(microsecond=0).isoformat()
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
    return render_template(_main_template(), msg=msg, title=title)


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
        _main_template(), subtemplate_name="client.html", msg=msg, title=title
    )


@app.get("/ws_news")
def ws_news():
    title, msg = "Websockets", "WS test"
    return render_template(
        _main_template(), subtemplate_name="ws.html", msg=msg, title=title
    )


@sock.route("/echo_ws")
def echo_ws(ws):
    # import sys
    # from pprint import pprint

    while True:
        if data := ws.receive(timeout=0.25):
            # print("---", file=sys.stderr)
            # print("DATA:", file=sys.stderr)
            # pprint(data, stream=sys.stderr)
            # print("---", file=sys.stderr)
            if json.loads(data).get("cmd") == "stop":
                break
        else:
            now = datetime.now().replace(microsecond=0).isoformat()
            ws.send(f'<li id="current-time">Even more breaking news at: {now}</li>')
            sleep(2)

    ws.close()
    # ws.close(1_000, "User-requested shutdown.")


def _is_hx_req():
    return request.headers.get("HX-Request", "false") == "true"


def _main_template():
    return "partial.html" if _is_hx_req() else "index.html"


@app.context_processor
def _inject_global_template_vars():
    return {"current_year": date.today().year}
