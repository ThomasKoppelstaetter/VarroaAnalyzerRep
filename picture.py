from sql_functions import create_bild, update_zelle_stadium
import os
from camera import Camera
from ultralytics import YOLO

BASE_DIR = "static/captures"

# Modell einmalig laden
model = YOLO('best.pt')  # ← ggf. Pfad anpassen


def build_filename(wabe_id, posX, posY, richtung):
    filename = f"z_{posY:02d}_{posX:02d}_{richtung}.jpg"
    folder = os.path.join(BASE_DIR, f"wabe_{wabe_id}")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, filename), filename


def take(camera: Camera, wabe_id, zID, posX, posY, richtung):
    full_path, filename = build_filename(wabe_id, posX, posY, richtung)

    # Bild aufnehmen
    camera.capture_image(full_path)

    # YOLO Auswertung
    results = model(full_path)

    varroa_count = 0
    stadium = None
    max_conf = 0.0

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls)
            conf = float(box.conf)
            class_name = model.names[cls_id]

            if class_name == 'varroa':
                varroa_count += 1
            elif class_name.startswith('stadium_') and conf > max_conf:
                stadium = class_name
                max_conf = conf

    # Annotiertes Bild überschreiben
    results[0].save(filename=full_path)

    # In Datenbank speichern
    create_bild(
        zID=zID,
        namen=filename,
        pfad=full_path,
        varroaanzahl=varroa_count
    )

    # Stadium nur bei "oben" aktualisieren (wenn vorhanden)
    if richtung == "oben":
        update_zelle_stadium(zID, stadium)


# Testaufruf
if __name__ == "__main__":
    cam = Camera()
    take(cam, 1, 1, 15, 0, "oben")
    cam.release()