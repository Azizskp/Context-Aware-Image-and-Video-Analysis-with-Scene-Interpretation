import cv2
import os
from ultralytics import YOLO

from models.yolo_model import detect_objects
from context.context_logic import interpret_scene


def process_video(input_path, output_path="output/output_final.avi"):
    os.makedirs("output", exist_ok=True)

    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Error opening video")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 20

    fourcc = cv2.VideoWriter_fourcc(*'avc1')

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not out.isOpened():
        print("Error: VideoWriter failed")
        return

    # Load YOLO once
    model = YOLO("yolov8n.pt")

    frame_count = 0
    frame_skip = 2

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        # Skip frames for speed
        if frame_count % frame_skip != 0:
            continue

        # =========================
        # OBJECT DETECTION
        # =========================

        objects = detect_objects(frame)

        # =========================
        # SCENE INTERPRETATION
        # =========================

        scene = interpret_scene(objects)

        # =========================
        # YOLO DETECTION
        # =========================

        results = model(frame, conf=0.25)

        for r in results:
            for box in r.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cls = int(box.cls[0])

                label = model.names[cls]

                conf = float(box.conf[0])

                # Bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Label
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        # =========================
        # SMART SCENE TEXT DISPLAY
        # =========================

        max_width = width - 40

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        thickness = 2

        words = scene.split()

        lines = []
        current_line = ""

        for word in words:

            test_line = current_line + word + " "

            (text_w, _), _ = cv2.getTextSize(
                test_line,
                font,
                font_scale,
                thickness
            )

            if text_w < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

        # Draw wrapped scene text
        y = 40

        for line in lines:

            (text_w, text_h), _ = cv2.getTextSize(
                line,
                font,
                font_scale,
                thickness
            )

            cv2.rectangle(
                frame,
                (15, y - 30),
                (25 + text_w, y + 10),
                (0, 0, 0),
                -1
            )

            cv2.putText(
                frame,
                line,
                (20, y),
                font,
                font_scale,
                (0, 255, 255),
                thickness,
                cv2.LINE_AA
            )

            y += 40

       # =========================
# OBJECT COUNT DISPLAY
# =========================

        obj_text = ", ".join(
            [f"{k}:{v}" for k, v in objects.items()]
        )

# Background for object text
        (obj_w, obj_h), _ = cv2.getTextSize(
            obj_text,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            2
        )

        cv2.rectangle(
            frame,
            (15, y - 15),
            (25 + obj_w, y + 15),
            (0, 0, 0),
            -1
        )

# Bright white text
        cv2.putText(
         frame,
        obj_text,
        (20, y + 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA
)
        # =========================
        # FRAME INFO
        # =========================

        cv2.putText(
            frame,
            f"Frame: {frame_count}",
            (20, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        # =========================
        # WRITE FRAME
        # =========================

        out.write(frame)

        print(
            f"Frame {frame_count} | Scene: {scene}"
        )

    cap.release()
    out.release()

    print(
        f"\n✅ Final video saved at: {output_path}"
    )