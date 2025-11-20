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

def take():
    """Nimmt ein Bild auf und speichert es automatisch"""
    camera = Camera()
    save_path = get_next_filename()
    print(f"📸 Nehme Bild auf → {save_path}")
    camera.capture_image(save_path)
    camera.release()
    print("✅ Foto erfolgreich gespeichert!")
    return save_path

# Damit man picture.py auch standalone ausführen kann
if __name__ == "__main__":
    take()
