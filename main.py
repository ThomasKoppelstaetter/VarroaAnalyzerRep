import utils_stepper
import subprocess
import time
from camera import Camera
import picture

# Anzahl der Zellen in X- und Y-Richtung
x_Cells = 20
y_Cells = 10

try:
    camera = Camera()                  # Kamera einmalig initialisieren
    utils_stepper.setup()

    for y in range(y_Cells):
        for x in range(x_Cells):
            # Warten
            time.sleep(0.8)

            # Foto oben
            picture.take(camera)       # Kamera-Objekt übergeben
            time.sleep(0.5)

            # Wechselt auf Öffner
            utils_stepper.runCell_x(True, 8)

            # Geht nach unten
            utils_stepper.runMM_z(True, 20)

            # Öffnet Zelle (auskommentiert, falls Pumpe verwendet wird)
            # subprocess.run(['python3', 'open_cell.py'])

            # Geht nur teilweise nach oben
            utils_stepper.runMM_z(False, 10)
            time.sleep(0.8)

            # Foto unten
            picture.take(camera)
            time.sleep(0.5)

            # Geht nach oben
            utils_stepper.runMM_z(False, 10)

            # Wechselt zurück auf Öffner (falls benötigt)
            # utils_stepper.runCell_x(False, 3)

            # Geht zurück auf Kamera
            utils_stepper.runCell_x(False, 8)

            # Geht 1 nach links (nächste Spalte)
            utils_stepper.runCell_x(True, 1)

        # Nach einer kompletten Reihe: zurück an den Anfang der nächsten Reihe
        utils_stepper.runCell_y(False, 1)
        utils_stepper.runCell_x(False, x_Cells)

    # Alles fertig
    utils_stepper.runCell_y(True, y_Cells)
    utils_stepper.shutdown()
    print("Cells done")

except KeyboardInterrupt:
    print("Program terminated")
    camera.release()                   # Kamera im Fehlerfall freigeben
    utils_stepper.shutdown()