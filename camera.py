from picamera2 import Picamera2
import cv2
import time
import os

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (640, 480)}))
        self.picam2.start()

    def gen_frames(self):
        while True:
            frame = self.picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # 🔹 NEU: Funktion zum Aufnehmen eines einzelnen Bildes
    def capture_image(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"static/captures/image_{timestamp}.jpg"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.picam2.capture_file(filename)

    def release(self):
        self.picam2.stop()
