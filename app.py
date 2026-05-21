from flask import Flask, render_template, request, redirect
import os
import cv2
from ultralytics import YOLO

from models.yolo_model import detect_objects
from context.context_logic import interpret_scene
from video.process_video import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            return redirect(request.url)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        # =====================================
        # IMAGE PROCESSING
        # =====================================

        if file.filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):

            frame = cv2.imread(filepath)

            if frame is None:
                return "Error reading image"

            # Detect objects
            objects = detect_objects(frame)

            # Scene interpretation
            scene = interpret_scene(objects)

            print("Objects:", objects)
            print("Scene:", scene)

            # YOLO model
            model = YOLO("yolov8n.pt")

            results = model(frame, conf=0.25)

            # =====================================
            # DRAW BOUNDING BOXES
            # =====================================

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

                    # Label text
                    cv2.putText(
                        frame,
                        f"{label} {conf:.2f}",
                        (x1, max(y1 - 5, 50)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2
                    )

            # =====================================
            # CLEAN TOP LABEL
            # =====================================

            height, width = frame.shape[:2]

            # Shorten long scene text
            max_chars = 35

            display_scene = scene

            if len(scene) > max_chars:
                display_scene = scene[:max_chars] + "..."

            # Black top bar
            cv2.rectangle(
                frame,
                (0, 0),
                (width, 40),
                (0, 0, 0),
                -1
            )

            # Scene text
            cv2.putText(
                frame,
                display_scene,
                (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # =====================================
            # SAVE OUTPUT IMAGE
            # =====================================

            output_path = os.path.join(
                OUTPUT_FOLDER,
                "result.jpg"
            )

            cv2.imwrite(output_path, frame)

            return render_template(
                "index.html",
                output_file="output/result.jpg",
                scene=scene
            )

        # =====================================
        # VIDEO PROCESSING
        # =====================================

        elif file.filename.lower().endswith(
            (".mp4", ".avi", ".mov")
        ):

            output_path = os.path.join(
                OUTPUT_FOLDER,
                "result.mp4"
            )

            process_video(filepath, output_path)

            return render_template(
                "index.html",
                output_file="output/result.mp4",
                scene="Video processed"
            )

    return render_template(
        "index.html",
        output_file=None,
        scene=None
    )


if __name__ == "__main__":
    app.run(debug=True)