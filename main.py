# main.py
from sql_functions import create_wabe, create_zelle
import utils_stepper
import time
import signal
from camera import Camera
import picture

# =========================
# GLOBALE STEUERUNG
# =========================

running = True

def shutdown_handler(signum, frame):
    global running
    print("Shutdown-Signal empfangen")
    running = False

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

# =========================
# KONFIGURATION
# =========================

x_Cells = 20
y_Cells = 10

# =========================
# MAIN LOGIK
# =========================

def main():
    global running

    posX = 0
    posY = 0

    camera = None

    try:
        print("Main gestartet")

        camera = Camera()
        utils_stepper.setup()

        wID = create_wabe()
        print(f"Wabe erstellt: ID {wID}")

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

                # Optional: Zelle öffnen
                # subprocess.run(['python3', 'open_cell.py'])

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

        try:
            if camera:
                camera.release()
        except Exception as e:
            print("Fehler beim Kamera-Release:", e)

        try:
            utils_stepper.shutdown()
        except Exception as e:
            print("Fehler beim Stepper-Shutdown:", e)

        print("Main sauber beendet")

# =========================
# STARTPUNKT
# =========================

if __name__ == "__main__":
    main()
