from picamera2 import Picamera2
import cv2
import time
import os
import threading


class Camera:
    def __init__(self):
        self._frame = None
        self._new_frame = threading.Condition()
        self._running = True

        self.picam2 = self._create_and_start()

        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    def _create_and_start(self):
        cam = Picamera2()
        cam.configure(cam.create_preview_configuration(main={"size": (640, 480)}))
        cam.start()
        return cam

    def _capture_loop(self):
        """Leert den V4L2-Buffer kontinuierlich. Startet die Kamera neu bei Pipeline-Crash."""
        while self._running:
            try:
                frame = self.picam2.capture_array()
                with self._new_frame:
                    self._frame = frame
                    self._new_frame.notify_all()
            except Exception as e:
                print(f"[Camera] Pipeline-Fehler: {e} — starte Kamera neu...")
                self._restart()

    def _restart(self):
        try:
            self.picam2.stop()
        except Exception:
            pass
        try:
            self.picam2.close()
        except Exception:
            pass

        time.sleep(2.0)

        try:
            self.picam2 = self._create_and_start()
            print("[Camera] Kamera erfolgreich neu gestartet")
        except Exception as e:
            print(f"[Camera] Neustart fehlgeschlagen: {e}")
            time.sleep(5.0)

    def gen_frames(self):
        while True:
            with self._new_frame:
                self._new_frame.wait(timeout=2.0)
                frame = self._frame
            if frame is None:
                continue
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
            self._new_frame.wait(timeout=5.0)
            frame = self._frame
        if frame is not None:
            cv2.imwrite(filename, frame)

    def release(self):
        self._running = False
        self._thread.join(timeout=3.0)
        try:
            self.picam2.stop()
        except Exception:
            pass
