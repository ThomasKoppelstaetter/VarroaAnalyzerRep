from sql_functions import create_bild
import os
from camera import Camera

BASE_DIR = "static/captures"


def build_filename(wabe_id, posX, posY, richtung):
    """Erzeugt den Dateinamen nach deinem gewünschten Format."""
    filename = f"z_{posY:02d}_{posX:02d}_{richtung}.jpg"
    folder = os.path.join(BASE_DIR, f"wabe_{wabe_id}")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename), filename


def take(camera: Camera, wabe_id, zID, posX, posY, richtung):
    """
    Nimmt ein Bild mit der Kamera auf,
    speichert es in static/captures/wabe_X/
    und trägt es in die SQL Datenbank ein.
    """
    full_path, filename = build_filename(wabe_id, posX, posY, richtung)

    print(f"📸 Nehme Bild auf → {full_path}")
    camera.capture_image(full_path)   # Bild speichern
    print("✅ Foto erfolgreich gespeichert!")

    # SQL-Eintrag erzeugen
    create_bild(
        zID=zID,
        namen=filename,
        pfad=full_path,
        varroaanzahl=None
    )

    print("📁 Bild wurde in der Datenbank eingetragen!")

    return full_path


# Nur zum Testen falls picture.py direkt aufgerufen wird
if __name__ == "__main__":
    cam = Camera()
    take(cam, 1, 1, 15, 0, "oben")
    cam.release()
