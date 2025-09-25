from flask import Flask, render_template, redirect, url_for
import subprocess, signal, os

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 0.0.0.0 = erreichbar im lokalen Netz
