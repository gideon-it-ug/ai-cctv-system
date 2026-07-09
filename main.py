from dotenv import load_dotenv
import os

load_dotenv()

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")
WHATSAPP_APIKEY = os.getenv("WHATSAPP_APIKEY")
DJANGO_IP = os.getenv("DJANGO_IP")

import cv2
from detector.person_detector import PersonDetector
from notifier import WhatsAppNotifier
from api_client import EventAPIClient
import time
# --- Config ---
CAMERA_NAME = "Camera 1"
WHATSAPP_PHONE = "256740797259"   # your number, international format, no +
WHATSAPP_APIKEY = "YOUR_APIKEY"   # from CallMeBot
DJANGO_IP = "192.168.1.4"       # replace with YOUR laptop's IP from ipconfig

detector = PersonDetector(confidence_threshold=0.5, cooldown_seconds=120)
notifier = WhatsAppNotifier(WHATSAPP_PHONE, WHATSAPP_APIKEY)
api_client = EventAPIClient(base_url=f"http://{DJANGO_IP}:8000/api/events/")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("System running. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    annotated_frame, person_detected, confidence = detector.detect(frame)

    if person_detected and detector.should_alert():
        print(f"ALERT: Person detected! Confidence: {confidence:.2f}")

        image_url = api_client.send_event(CAMERA_NAME, "person", confidence, frame)

        message = f"SECURITY ALERT - Person detected on {CAMERA_NAME} - Confidence: {confidence:.0%}"
        if image_url:
            message += f" - View image: {image_url}"

        notifier.send_alert(message)

    cv2.imshow("AI CCTV", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

last_heartbeat = 0
HEARTBEAT_INTERVAL = 5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()
    if now - last_heartbeat > HEARTBEAT_INTERVAL:
        api_client.send_heartbeat(CAMERA_NAME)
        last_heartbeat = now

    annotated_frame, person_detected, confidence = detector.detect(frame)
    # ... rest stays the same