# picture.py
import os
from camera import Camera

SAVE_DIR = "static/captures"

def get_next_filename():
    """Finde den nächsten freien Bildnamen (image1.jpg, image2.jpg, …)"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    i = 1
    while True:
        filename = f"image{i}.jpg"
        filepath = os.path.join(SAVE_DIR, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1

def take(camera: Camera):
    """
    Nimmt ein Bild mit der bereits initialisierten Kamera auf.
    WICHTIG: Die Kamera wird NICHT released – das macht main.py am Ende!
    """
    save_path = get_next_filename()
    print(f"Nehme Bild auf → {save_path}")
    camera.capture_image(save_path)   # benutze die übergebene Kamera
    print("Foto erfolgreich gespeichert!")
    return save_path

# Nur zum Testen, wenn man picture.py direkt ausführt
if __name__ == "__main__":
    cam = Camera()
    take(cam)
    cam.release()