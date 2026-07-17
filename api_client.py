import requests
import cv2
import io


class EventAPIClient:
    def __init__(self, base_url="http://192.168.1.4:8000/api/events/"):
        self.base_url = base_url

    def send_event(self, camera_name, event_type, confidence, frame, person_count=0, plate_number=None):
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            print("Failed to encode frame")
            return None

        files = {'image': ('event.jpg', io.BytesIO(buffer), 'image/jpeg')}
        data = {
            'camera_name': camera_name,
            'event_type': event_type,
            'confidence': confidence,
            'person_count': person_count,
        }
        if plate_number:
            data['plate_number'] = plate_number

        try:
            response = requests.post(self.base_url, data=data, files=files, timeout=10)
            print(f"Event sent to API: {response.status_code}")
            if response.status_code == 201:
                return response.json().get('image')
            return None
        except Exception as e:
            print(f"Failed to send event to API: {e}")
            return None

    def send_heartbeat(self, camera_name):
        try:
            requests.post(
                self.base_url.replace('events/', 'cameras/heartbeat/'),
                data={'camera_name': camera_name},
                timeout=5
            )
        except Exception as e:
            print(f"Heartbeat failed: {e}")