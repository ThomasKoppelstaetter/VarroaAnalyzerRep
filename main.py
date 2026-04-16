# main.py
from sql_functions import create_wabe, create_zelle
import utils_stepper
import picture
import requests
import subprocess
import os

# =========================
# KONFIGURATION
# =========================

x_Cells = 20
y_Cells = 10

STECKDOSE_IP = "http://172.20.10.5"

# Versatz vom Öffner (Nullpunkt)
KAMERA_OFFSET = 8   # Kamera ist +8 Zellen vom Öffner
PUMPE_OFFSET  = 3   # Pumpe ist -3 Zellen vom Öffner

# =========================
# HILFSFUNKTIONEN
# =========================

def steckdose(ein: bool):
    cmd = "Power%20On" if ein else "Power%20Off"
    try:
        requests.get(f"{STECKDOSE_IP}/cm?cmnd={cmd}", timeout=3)
        print(f"Steckdose {'ein' if ein else 'aus'}")
    except requests.RequestException as e:
        print(f"Steckdose nicht erreichbar: {e}")

def open_cell():
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "open_cell.py")
    subprocess.run(["python3", script])
    print("Zelle ist geöffnet")

# =========================
# MAIN LOGIK ALS FUNKTION
# =========================

running = True

def stop_scan():
    global running
    running = False

def main_scan(camera):
    """Führt den Zell-Scan durch. Kamera wird übergeben."""
    global running
    running = True

    print("Main Scan gestartet")

    wID = create_wabe()
    print(f"Wabe erstellt: ID {wID}")

    try:
        for y in range(y_Cells):
            if not running:
                break

            for x in range(x_Cells):
                if not running:
                    break

                print(f"--- Zelle X={x}, Y={y} ---")

                zID = create_zelle(wID, x, y)

                # 1. Zelle öffnen (Öffner ist Nullpunkt, bereits über der Zelle)
                utils_stepper.runMM_z(True, 20)
                open_cell()
                utils_stepper.runMM_z(False, 20)

                # 2. Foto oben (Kamera ist +8 vom Öffner)
                utils_stepper.runCell_x(False, KAMERA_OFFSET)   # Kamera über Zelle
                utils_stepper.runMM_z(True, 20)
                picture.take(camera, wID, zID, x, y, "oben")
                utils_stepper.runMM_z(False, 20)
                utils_stepper.runCell_x(True, KAMERA_OFFSET)    # zurück zum Öffner

                # 3. Vakuumpumpe über Zelle (Pumpe ist -3 vom Öffner)
                utils_stepper.runCell_x(True, PUMPE_OFFSET)     # Pumpe über Zelle
                utils_stepper.runMM_z(True, 20)
                steckdose(True)
                utils_stepper.runMM_z(False, 20)
                steckdose(False)
                utils_stepper.runCell_x(False, PUMPE_OFFSET)    # zurück zum Öffner

                # 4. Foto unten (wieder Kamera über Zelle)
                utils_stepper.runCell_x(False, KAMERA_OFFSET)   # Kamera über Zelle
                utils_stepper.runMM_z(True, 20)
                picture.take(camera, wID, zID, x, y, "unten")
                utils_stepper.runMM_z(False, 20)
                utils_stepper.runCell_x(True, KAMERA_OFFSET)    # zurück zum Öffner

                # 5. Nächste Zelle
                utils_stepper.runCell_x(True, 1)

            # Neue Reihe: X zurücksetzen, Y weiter
            utils_stepper.runCell_y(False, 1)
            utils_stepper.runCell_x(False, x_Cells)

        print("Scan abgeschlossen")

    finally:
        print("Cleanup läuft...")
        utils_stepper.shutdown()
        print("Main sauber beendet")
