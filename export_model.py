from ultralytics import YOLO

model = YOLO("yolo11n.pt")
model.export(format="openvino")

print("Export complete! Look for the 'yolo11n_openvino_model' folder in this directory.")