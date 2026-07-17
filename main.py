import cv2
import time
from detector.yolo_engine import YOLOEngine
from detector.person_detector import PersonDetector
from detector.object_tracker import AbandonedObjectTracker, STATIONARY_THRESHOLD_SECONDS
from detector.plate_reader import PlateReader
from notifier import WhatsAppNotifier
from api_client import EventAPIClient

# --- Config ---
CAMERA_NAME = "Camera 1"
WHATSAPP_PHONE = "256740797259"   # your number, international format, no +
WHATSAPP_APIKEY = "2938366"   # from CallMeBot
DJANGO_IP = "192.168.1.4"         # your laptop's IP
FRAME_SKIP = 3
PLATE_CHECK_EVERY = 15            # run OCR less often, it's heavier than detection

engine = YOLOEngine(model_path="yolo11n_openvino_model/")
person_detector = PersonDetector(confidence_threshold=0.5, cooldown_seconds=120)
object_tracker = AbandonedObjectTracker()
plate_reader = PlateReader()
notifier = WhatsAppNotifier(WHATSAPP_PHONE, WHATSAPP_APIKEY)
api_client = EventAPIClient(base_url=f"http://{DJANGO_IP}:8000/api/events/")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("System running. Press 'q' to quit.")

last_heartbeat = 0
HEARTBEAT_INTERVAL = 5
frame_counter = 0
last_display_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    if now - last_heartbeat > HEARTBEAT_INTERVAL:
        api_client.send_heartbeat(CAMERA_NAME)
        last_heartbeat = now

    frame_counter += 1

    if frame_counter % FRAME_SKIP == 0:
        result = engine.infer(frame)
        names = engine.names

        person_detected, confidence, person_count, person_boxes = person_detector.analyze(result, names)
        abandoned_objects = object_tracker.update(result, names, person_boxes)

        annotated_frame = result.plot()
        cv2.putText(
            annotated_frame,
            f"People: {person_count}",
            (15, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (61, 220, 132),
            2,
        )
        last_display_frame = annotated_frame

        # --- Person alert ---
        if person_detected and person_detector.should_alert():
            print(f"ALERT: {person_count} person(s) detected! Confidence: {confidence:.2f}")
            image_url = api_client.send_event(CAMERA_NAME, "person", confidence, frame, person_count)
            message = (
                f"SECURITY ALERT - {person_count} person(s) detected on {CAMERA_NAME} "
                f"- Confidence: {confidence:.0%}"
            )
            if image_url:
                message += f" - View image: {image_url}"
            notifier.send_alert(message)

        # --- Abandoned object alert(s) ---
        for obj in abandoned_objects:
            print(f"ALERT: Abandoned {obj.class_name} detected!")
            image_url = api_client.send_event(CAMERA_NAME, "abandoned_object", 1.0, frame, 0)
            message = (
                f"SECURITY ALERT - Abandoned {obj.class_name} detected on {CAMERA_NAME}, "
                f"unattended for over {STATIONARY_THRESHOLD_SECONDS} seconds"
            )
            if image_url:
                message += f" - View image: {image_url}"
            notifier.send_alert(message)

        # --- License plate check (less frequent, OCR is heavy) ---
        if frame_counter % PLATE_CHECK_EVERY == 0:
            plates = plate_reader.read_plates(frame, result, names)
            for plate_text, box in plates:
                print(f"ALERT: License plate detected - {plate_text}")
                image_url = api_client.send_event(
                    CAMERA_NAME, "license_plate", 0.8, frame, 0, plate_number=plate_text
                )
                message = f"VEHICLE DETECTED - Plate: {plate_text} on {CAMERA_NAME}"
                if image_url:
                    message += f" - View image: {image_url}"
                notifier.send_alert(message)

    else:
        last_display_frame = frame

    cv2.imshow("AI CCTV", last_display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()