import cv2
import time
from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_path="yolo11n.pt", confidence_threshold=0.5, cooldown_seconds=10):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = 0

    def detect(self, frame):
        """
        Runs detection on a frame.
        Returns (annotated_frame, person_detected: bool, confidence: float)
        """
        results = self.model(frame, verbose=False)
        annotated_frame = results[0].plot()

        person_detected = False
        best_confidence = 0.0

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = float(box.conf[0])

            if class_name == "person" and confidence > self.confidence_threshold:
                person_detected = True
                best_confidence = max(best_confidence, confidence)

        return annotated_frame, person_detected, best_confidence

    def should_alert(self):
        """
        Returns True if enough time has passed since the last alert (cooldown logic).
        """
        now = time.time()
        if now - self.last_alert_time >= self.cooldown_seconds:
            self.last_alert_time = now
            return True
        return False