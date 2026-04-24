from picamera2 import Picamera2
import cv2
import time
import os
import threading


class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (640, 480)}))
        self.picam2.start()

        self._frame = None
        self._new_frame = threading.Condition()
        self._running = True

        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    def _capture_loop(self):
        """Leert den V4L2-Buffer kontinuierlich, unabhängig vom Stream."""
        while self._running:
            frame = self.picam2.capture_array()
            with self._new_frame:
                self._frame = frame
                self._new_frame.notify_all()

    def gen_frames(self):
        while True:
            with self._new_frame:
                self._new_frame.wait()
                frame = self._frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def capture_image(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"static/captures/image_{timestamp}.jpg"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with self._new_frame:
            self._new_frame.wait()
            frame = self._frame
        cv2.imwrite(filename, frame)

    def release(self):
        self._running = False
        self._thread.join(timeout=2.0)
        self.picam2.stop()
