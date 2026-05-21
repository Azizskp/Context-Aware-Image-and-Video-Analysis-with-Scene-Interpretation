import os
import cv2

from ultralytics import YOLO
from models.yolo_model import detect_objects
from context.context_logic import interpret_scene
from video.process_video import process_video


DATA_FOLDER = "data"


def process_image(file_path):
    print(f"\nProcessing Image: {file_path}")

    frame = cv2.imread(file_path)

    if frame is None:
        print("Error: Could not read image")
        return

    objects = detect_objects(frame)
    scene = interpret_scene(objects)

    print("Objects:", objects)
    print("Scene:", scene)

    # Draw boxes
    model = YOLO("yolov8n.pt")
    results = model(frame)

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

    # Add scene text
    cv2.putText(frame, scene, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 0, 255), 2)

    os.makedirs("output", exist_ok=True)
    cv2.imwrite("output/result.jpg", frame)

    print("Saved → output/result.jpg")


def process_all():
    print("Scanning data folder...")

    if not os.path.exists(DATA_FOLDER):
        print("❌ data folder not found")
        return

    files = os.listdir(DATA_FOLDER)

    if not files:
        print("❌ No files inside data folder")
        return

    for file in files:
        file_path = os.path.join(DATA_FOLDER, file)

        print(f"Found file: {file}")

        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            process_image(file_path)

        elif file.lower().endswith((".mp4", ".avi", ".mov")):
            print(f"\nProcessing Video: {file_path}")
            process_video(file_path)

        else:
            print(f"Skipping unsupported file: {file}")


if __name__ == "__main__":
    process_all()