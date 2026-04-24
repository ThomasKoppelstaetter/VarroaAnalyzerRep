from picamera2 import Picamera2
import cv2
import time
import os
import threading


class Camera:
    def __init__(self):
        self._frame = None
        self._last_frame_time = 0.0
        self._new_frame = threading.Condition()
        self._running = True
        self._capture_gen = 0  # Generationszähler um alte hängende Threads zu stoppen

        self.picam2 = self._create_and_start()
        self._start_capture_thread()

        self._watchdog_thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog_thread.start()

    def _create_and_start(self):
        cam = Picamera2()
        config = cam.create_preview_configuration(
            main={"size": (640, 480)},
            controls={"FrameDurationLimits": (66666, 66666)}  # 15fps statt 30fps → halbe DMA-Last
        )
        cam.configure(config)
        cam.start()
        return cam

    def _start_capture_thread(self):
        gen = self._capture_gen
        threading.Thread(target=self._capture_loop, args=(gen,), daemon=True).start()

    def _capture_loop(self, gen):
        while self._running and gen == self._capture_gen:
            try:
                frame = self.picam2.capture_array()
                self._last_frame_time = time.time()
                with self._new_frame:
                    self._frame = frame
                    self._new_frame.notify_all()
            except Exception as e:
                if gen == self._capture_gen:
                    print(f"[Camera] Fehler: {e}")
                return

    def _watchdog_loop(self):
        # Startup-Zeit abwarten bevor Watchdog aktiv wird
        time.sleep(5.0)
        self._last_frame_time = time.time()

        while self._running:
            time.sleep(3.0)
            if self._running and (time.time() - self._last_frame_time) > 3.0:
                print("[Camera] Watchdog: keine Frames seit 3s — starte Kamera neu...")
                self._do_restart()

    def _do_restart(self):
        self._capture_gen += 1  # Alten hängenden capture_loop-Thread invalidieren
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
            self._last_frame_time = time.time()
            self._start_capture_thread()
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
            _, buffer = cv2.imencode('.jpg', frame)
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
        try:
            self.picam2.stop()
        except Exception:
            pass
