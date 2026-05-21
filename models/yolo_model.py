from ultralytics import YOLO

# Load model once
model = YOLO("yolov8n.pt")

def detect_objects(frame):
    results = model(frame)

    detected = {}

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = model.names[cls]

            detected[name] = detected.get(name, 0) + 1

    return detected