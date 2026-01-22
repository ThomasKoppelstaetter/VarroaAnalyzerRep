# main.py
from sql_functions import create_wabe, create_zelle
import utils_stepper
import time
import picture

# =========================
# KONFIGURATION
# =========================

x_Cells = 20
y_Cells = 10

# =========================
# MAIN LOGIK ALS FUNKTION
# =========================

running = True  # global für Stop-Signal

def stop_scan():
    global running
    running = False

def main_scan(camera):
    """Führt den Zell-Scan durch. Kamera wird übergeben."""
    global running

    posX = 0
    posY = 0

    print("Main Scan gestartet")

    utils_stepper.setup()

    wID = create_wabe()
    print(f"Wabe erstellt: ID {wID}")

    try:
        for y in range(y_Cells):
            if not running:
                break

            for x in range(x_Cells):
                if not running:
                    break

                print(f"Zelle X={posX}, Y={posY}")

                zID = create_zelle(wID, posX, posY)
                time.sleep(0.8)

                # Foto oben
                picture.take(camera, wID, zID, posX, posY, "oben")
                time.sleep(0.5)

                # Öffnerposition
                utils_stepper.runCell_x(True, 8)

                # Nach unten
                utils_stepper.runMM_z(True, 20)

                # Teilweise hoch
                utils_stepper.runMM_z(False, 10)
                time.sleep(0.8)

                # Foto unten
                picture.take(camera, wID, zID, posX, posY, "unten")
                time.sleep(0.5)

                # Ganz hoch
                utils_stepper.runMM_z(False, 10)

                # Zurück zur Kamera
                utils_stepper.runCell_x(False, 8)

                # Nächste Zelle
                utils_stepper.runCell_x(True, 1)
                posX += 1

            # Neue Reihe
            posY += 1
            posX = 0
            utils_stepper.runCell_y(False, 1)
            utils_stepper.runCell_x(False, x_Cells)

        print("Scan abgeschlossen")

    finally:
        print("Cleanup läuft...")
        utils_stepper.shutdown()
        print("Main sauber beendet")
