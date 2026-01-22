from flask import Flask, render_template, Response, redirect, url_for
import subprocess, signal, os, requests
import utils_stepper
import threading
from camera import Camera  # nutzt picamera2
from sql_functions import get_waben, get_zellen_by_wabe
from flask import request


app = Flask(__name__)
camera = Camera()  # Kamera initialisieren
process = None     # Für test_stepper.py

utils_stepper.setup()

# ----------- Routen -----------

@app.route("/")
def index():
    wID = request.args.get("wID", type=int)

    waben = get_waben()
    zellen = get_zellen_by_wabe(wID) if wID else []

    return render_template(
        "index.html",
        waben=waben,
        selected_wID=wID,
        zellen=zellen
    )

@app.route("/live")
def live():
    return render_template("live.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

# ----------- Kamera-Stream -----------

@app.route("/video_feed")
def video_feed():
    """Video-Stream der Kamera"""
    return Response(camera.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ----------- Stepper Motor Steuerung -----------

@app.route("/start")
def start():
    global process
    if process is None:
        main_path = os.path.join(os.path.dirname(__file__), "main.py")
        process = subprocess.Popen(["python3", main_path])
    return redirect(url_for("settings"))

@app.route("/stop")
def stop():
    global process
    if process is not None:
        process.terminate()  # sendet SIGTERM
        process.wait(timeout=5)
        process = None
    return redirect(url_for("settings"))

# ======== Motorsteuerung ========
@app.route("/move/<axis>/<direction>")
def move(axis, direction):
    def run():
        if axis == "x":
            utils_stepper.runMM_x(direction == "forward", 10)
        elif axis == "y":
            utils_stepper.runMM_y(direction == "forward", 10)
        elif axis == "z":
            utils_stepper.runMM_z(direction == "forward", 10)
        else:
            print("Ungültige Achse")

    # Thread starten, damit Flask nicht blockiert
    threading.Thread(target=run).start()
    return redirect(url_for("settings"))


# ----------- WLAN-Steckdose Steuerung -----------

@app.route("/steckdose/ein")
def steckdose_ein():
    """Schaltet WLAN-Steckdose ein"""
    ip = "http://172.20.10.5"  # IP-Adresse deiner Tasmota-Steckdose
    try:
        requests.get(f"{ip}/cm?cmnd=Power%20On", timeout=3)
    except requests.RequestException:
        pass
    return redirect(url_for("settings"))

@app.route("/steckdose/aus")
def steckdose_aus():
    """Schaltet WLAN-Steckdose aus"""
    ip = "http://172.20.10.5"
    try:
        requests.get(f"{ip}/cm?cmnd=Power%20Off", timeout=3)
    except requests.RequestException:
        pass
    return redirect(url_for("settings"))

# ----------- Hauptprogramm -----------

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False)
    finally:
        try:
            camera.release()
        except Exception as e:
            print("Kamera konnte nicht freigegeben werden:", e)
        try:
            utils_stepper.shutdown()
        except Exception as e:
            print("Stepper konnte nicht beendet werden:", e)
