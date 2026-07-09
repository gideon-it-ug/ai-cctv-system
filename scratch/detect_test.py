import cv2
from ultralytics import YOLO

# Load the lightweight YOLO model (auto-downloads first time)
model = YOLO("yolo11n.pt")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

print("Detection running. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO detection on this frame
    results = model(frame, verbose=False)

    # Draw boxes + labels on the frame
    annotated_frame = results[0].plot()

    cv2.imshow("AI CCTV - Person Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()