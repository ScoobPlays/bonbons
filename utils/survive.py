from flask import Flask
from threading import Thread
import os
import logging

app = Flask("")

log = logging.getLogger("werkzeug")
log.disabled = True


@app.route("/")
def main():
    return "Your bot is alive!"


def run():
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    app.run(host="0.0.0.0", port=8080)


def survive():
    server = Thread(target=run)
    server.start()
