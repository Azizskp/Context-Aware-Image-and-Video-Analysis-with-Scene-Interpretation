import cv2

from models.yolo_model import detect_objects
from context.openrouter_context import generate_scene_description


image_path = "data/test.jpg"

frame = cv2.imread(image_path)

if frame is None:
    print("Error reading image")
    exit()

# YOLO detection
objects = detect_objects(frame)

print("Detected Objects:")
print(objects)

# OpenRouter reasoning
scene = generate_scene_description(objects)

print("\nAI Scene Description:")
print(scene)