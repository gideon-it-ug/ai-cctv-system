import time

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle"}
ANIMAL_CLASSES = {"dog", "cat"}


class PersonDetector:
    def __init__(self, confidence_threshold=0.5, cooldown_seconds=120):
        self.confidence_threshold = confidence_threshold
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time = 0
        self.last_vehicle_alert_time = 0
        self.last_animal_alert_time = 0

    def analyze(self, result, names):
        """
        Extracts person, vehicle, and animal detections from a YOLO result.
        Returns a dict with counts, confidences, and boxes for each category.
        """
        person_detected = False
        person_confidence = 0.0
        person_count = 0
        person_boxes = []

        vehicle_detected = False
        vehicle_confidence = 0.0
        vehicle_type = None

        animal_detected = False
        animal_confidence = 0.0
        animal_type = None

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = names[class_id]
            confidence = float(box.conf[0])

            if confidence < self.confidence_threshold:
                continue

            if class_name == "person":
                person_detected = True
                person_count += 1
                person_confidence = max(person_confidence, confidence)
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                person_boxes.append((x1, y1, x2, y2))

            elif class_name in VEHICLE_CLASSES:
                if confidence > vehicle_confidence:
                    vehicle_detected = True
                    vehicle_confidence = confidence
                    vehicle_type = class_name

            elif class_name in ANIMAL_CLASSES:
                if confidence > animal_confidence:
                    animal_detected = True
                    animal_confidence = confidence
                    animal_type = class_name

        return {
            "person_detected": person_detected,
            "person_confidence": person_confidence,
            "person_count": person_count,
            "person_boxes": person_boxes,
            "vehicle_detected": vehicle_detected,
            "vehicle_confidence": vehicle_confidence,
            "vehicle_type": vehicle_type,
            "animal_detected": animal_detected,
            "animal_confidence": animal_confidence,
            "animal_type": animal_type,
        }

    def should_alert_person(self):
        now = time.time()
        if now - self.last_alert_time >= self.cooldown_seconds:
            self.last_alert_time = now
            return True
        return False

    def should_alert_vehicle(self):
        now = time.time()
        if now - self.last_vehicle_alert_time >= self.cooldown_seconds:
            self.last_vehicle_alert_time = now
            return True
        return False

    def should_alert_animal(self):
        now = time.time()
        if now - self.last_animal_alert_time >= self.cooldown_seconds:
            self.last_animal_alert_time = now
            return True
        return False