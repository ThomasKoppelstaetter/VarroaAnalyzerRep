from flask import Flask, render_template, Response, redirect, url_for
import subprocess, signal, os
import requests
from camera import Camera

app = Flask(__name__)
camera = Camera()
process = None  # Für test_stepper.py

# --------- Routes ---------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/live")
def live():
    return render_template("live.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/video_feed")
def video_feed():
    return Response(camera.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --------- Stepper Kontrolle ---------
@app.route("/start")
def start():
    global process
    if process is None:
        process = subprocess.Popen(["python3", "test_stepper.py"])
    return redirect(url_for("settings"))

@app.route("/stop")
def stop():
    global process
    if process is not None:
        os.kill(process.pid, signal.SIGTERM)
        process = None
    return redirect(url_for("settings"))

# --------- Steckdose Kontrolle ---------
@app.route("/steckdose/ein")
def steckdose_ein():
    ip = "http://172.20.10.5"
    url = f"{ip}/cm?cmnd=Power%20On"
    requests.get(url)
    return redirect(url_for("settings"))

@app.route("/steckdose/aus")
def steckdose_aus():
    ip = "http://172.20.10.5"
    url = f"{ip}/cm?cmnd=Power%20Off"
    requests.get(url)
    return redirect(url_for("settings"))

# --------- App starten ---------
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        camera.release()
