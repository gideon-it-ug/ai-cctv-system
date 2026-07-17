import re
import time
import easyocr

VEHICLE_CLASSES = {"car", "truck", "bus", "motorcycle"}
PLATE_PATTERN = re.compile(r'^[A-Z0-9]{4,10}$')
PLATE_COOLDOWN_SECONDS = 300  # don't re-alert same plate for 5 minutes


class PlateReader:
    def __init__(self):
        print("Loading OCR model (first run may take a moment)...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        self.recent_plates = {}  # plate_text -> last_alert_time

    def read_plates(self, frame, result, names):
        """
        Crops each detected vehicle box and runs OCR to find plate-like text.
        Returns list of (plate_text, vehicle_box) for NEW plates only (not in cooldown).
        """
        new_plates = []
        h, w = frame.shape[:2]

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = names[class_id]
            confidence = float(box.conf[0])

            if class_name not in VEHICLE_CLASSES or confidence < 0.4:
                continue

            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            ocr_results = self.reader.readtext(crop)

            for (_, text, conf) in ocr_results:
                cleaned = text.upper().replace(" ", "").replace("-", "")

                if not PLATE_PATTERN.match(cleaned) or conf < 0.4:
                    continue

                now = time.time()
                last_seen = self.recent_plates.get(cleaned, 0)

                if now - last_seen >= PLATE_COOLDOWN_SECONDS:
                    self.recent_plates[cleaned] = now
                    new_plates.append((cleaned, (x1, y1, x2, y2)))

        return new_plates