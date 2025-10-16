from picamera2 import Picamera2
import time
import io

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.start()

    def gen_frames(self):
        while True:
            frame = self.picam2.capture_array()
            # Encode Frame zu JPEG
            import cv2
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def release(self):
        self.picam2.close()
