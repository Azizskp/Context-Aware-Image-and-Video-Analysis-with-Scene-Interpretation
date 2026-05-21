import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import cv2

# Load pretrained model
model = torch.hub.load(
    'pytorch/vision:v0.10.0',
    'deeplabv3_resnet50',
    pretrained=True
)
model.eval()

# COCO Labels
LABELS = [
    'background','aeroplane','bicycle','bird','boat','bottle','bus','car','cat',
    'chair','cow','diningtable','dog','horse','motorbike','person','pottedplant',
    'sheep','sofa','train','tv'
]

def segment_image(image_path, output_path="output/result.png"):
    image = Image.open(image_path).convert("RGB")

    transform = T.Compose([
        T.Resize(512),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])
    ])

    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)['out'][0]

    mask = output.argmax(0).byte().cpu().numpy()

    # Color mask
    colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    for label in np.unique(mask):
        color = np.random.randint(0, 255, size=3)
        colored_mask[mask == label] = color

    # Overlay
    original = np.array(image.resize((mask.shape[1], mask.shape[0])))
    overlay = cv2.addWeighted(original, 0.6, colored_mask, 0.4, 0)

    cv2.imwrite(output_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    return mask

def extract_labels(mask):
    unique, counts = np.unique(mask, return_counts=True)

    total_pixels = mask.size
    object_scores = []

    for label, count in zip(unique, counts):
        if label < len(LABELS):
            name = LABELS[label]

            if name == "background":
                continue

            ratio = count / total_pixels

            if ratio > 0.05:
                object_scores.append((name, ratio))

    # Sort by size
    object_scores.sort(key=lambda x: x[1], reverse=True)

    # Take top 2
    detected_objects = [obj[0] for obj in object_scores[:2]]

    return detected_objects