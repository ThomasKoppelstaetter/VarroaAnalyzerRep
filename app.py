from flask import Flask, render_template, redirect, url_for
import subprocess, signal, os
import requests

app = Flask(__name__)

process = None  # Speichert den Prozess von myscript.py

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    global process
    if process is None:
        process = subprocess.Popen(["python3", "test_stepper.py"])
    return redirect(url_for("index"))

@app.route("/stop")
def stop():
    global process
    if process is not None:
        os.kill(process.pid, signal.SIGTERM)
        process = None
    return redirect(url_for("index"))


@app.route("/steckdose/ein")
def steckdose_ein():
    ip = "http://172.20.10.5"  # IP-Adresse deiner Steckdose
    url = f"{ip}/cm?cmnd=Power%20On"
    requests.get(url)
    return redirect(url_for("index"))  # Zurück zur Startseite

@app.route("/steckdose/aus")
def steckdose_aus():
    ip = "http://172.20.10.5"  # IP-Adresse deiner Steckdose
    url = f"{ip}/cm?cmnd=Power%20Off"
    requests.get(url)
    return redirect(url_for("index"))  # Zurück zur Startseite

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Server starten
