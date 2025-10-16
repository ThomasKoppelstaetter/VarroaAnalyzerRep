import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # CSI-Kamera oder USB-Kamera

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def gen_frames(self):
        while True:
            frame = self.get_frame()
            if frame is None:
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def release(self):
        self.cap.release()
