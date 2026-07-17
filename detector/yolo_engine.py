from ultralytics import YOLO


class YOLOEngine:
    def __init__(self, model_path="yolo11n_openvino_model/"):
        self.model = YOLO(model_path)

    def infer(self, frame):
        results = self.model(frame, verbose=False)
        return results[0]

    @property
    def names(self):
        return self.model.names