import time


class PersonDetector:
    def __init__(self, confidence_threshold=0.5, cooldown_seconds=120):
        self.confidence_threshold = confidence_threshold
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = 0

    def analyze(self, result, names):
        """
        Extracts person detections from a YOLO result.
        Returns (person_detected, confidence, person_count, person_boxes)
        """
        person_detected = False
        best_confidence = 0.0
        person_count = 0
        person_boxes = []

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = names[class_id]
            confidence = float(box.conf[0])

            if class_name == "person" and confidence > self.confidence_threshold:
                person_detected = True
                person_count += 1
                best_confidence = max(best_confidence, confidence)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                person_boxes.append((x1, y1, x2, y2))

        return person_detected, best_confidence, person_count, person_boxes

    def should_alert(self):
        now = time.time()
        if now - self.last_alert_time >= self.cooldown_seconds:
            self.last_alert_time = now
            return True
        return False