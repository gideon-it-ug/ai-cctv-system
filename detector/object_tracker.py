import time

OBJECT_CLASSES = {"backpack", "handbag", "suitcase"}
STATIONARY_THRESHOLD_SECONDS = 15   # how long an object must stay still to count as abandoned
MOVEMENT_TOLERANCE_PX = 30          # centroid can drift this much and still count as "not moved"
PERSON_PROXIMITY_PX = 150           # a person within this distance "owns" the object
MAX_MATCH_DISTANCE_PX = 80          # max distance to match a detection to an existing tracked object
FORGET_AFTER_SECONDS = 5            # drop tracking if object hasn't been seen this long


class TrackedObject:
    def __init__(self, class_name, centroid, box):
        self.class_name = class_name
        self.centroid = centroid
        self.box = box
        self.stationary_since = time.time()
        self.last_seen = time.time()
        self.alerted = False

    def update(self, centroid, box):
        dx = centroid[0] - self.centroid[0]
        dy = centroid[1] - self.centroid[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > MOVEMENT_TOLERANCE_PX:
            self.stationary_since = time.time()
            self.alerted = False

        self.centroid = centroid
        self.box = box
        self.last_seen = time.time()

    def stationary_duration(self):
        return time.time() - self.stationary_since


class AbandonedObjectTracker:
    def __init__(self):
        self.tracked_objects = []

    def _centroid(self, box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def _distance(self, c1, c2):
        return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5

    def update(self, result, names, person_boxes):
        """
        Updates tracked objects using this frame's detections.
        Returns a list of TrackedObject instances newly flagged as abandoned this frame.
        """
        current_detections = []
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = names[class_id]
            confidence = float(box.conf[0])

            if class_name in OBJECT_CLASSES and confidence > 0.4:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                current_detections.append((class_name, (x1, y1, x2, y2)))

        person_centroids = [self._centroid(pb) for pb in person_boxes]

        for class_name, box in current_detections:
            centroid = self._centroid(box)

            best_match = None
            best_distance = MAX_MATCH_DISTANCE_PX
            for obj in self.tracked_objects:
                if obj.class_name != class_name:
                    continue
                dist = self._distance(obj.centroid, centroid)
                if dist < best_distance:
                    best_distance = dist
                    best_match = obj

            if best_match:
                best_match.update(centroid, box)
            else:
                self.tracked_objects.append(TrackedObject(class_name, centroid, box))

        self.tracked_objects = [
            obj for obj in self.tracked_objects
            if time.time() - obj.last_seen < FORGET_AFTER_SECONDS
        ]

        newly_abandoned = []
        for obj in self.tracked_objects:
            if obj.alerted:
                continue
            if obj.stationary_duration() < STATIONARY_THRESHOLD_SECONDS:
                continue

            has_nearby_person = any(
                self._distance(obj.centroid, pc) < PERSON_PROXIMITY_PX
                for pc in person_centroids
            )

            if not has_nearby_person:
                obj.alerted = True
                newly_abandoned.append(obj)

        return newly_abandoned