import os
import torch
import torchvision
from PIL import Image
import requests
from io import BytesIO
import transformers
model = torchvision.models.detection.retinanet_resnet50_fpn(pretrained=True)
model.eval()
from tavily import TavilyClient
# COCO class names
COCO_CLASSES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A',
    'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]
# Function to perform object detection using RetinaNet
def detect_objects(image_path):
    # Load the image
    image = Image.open(image_path).convert("RGB")
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
    ])
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    # Perform detection
    with torch.no_grad():
        detections = model(image_tensor)[0]
    # Extract detection results
    detected_objects = []
    labels = detections['labels']
    scores = detections['scores']
    boxes = detections['boxes']
    for label, score, box in zip(labels, scores, boxes):
        if score >= 0.5:  # Confidence threshold
            detected_objects.append({
                "label": COCO_CLASSES[label.item()],
                "score": score.item(),
                "bbox": box.tolist()
            })
    return detected_objects
# Convert detection results to textual format
def preprocess_detection_results(detected_objects):
    description = "The image contains: "
    for obj in detected_objects:
        label = obj['label']
        bbox = obj['bbox']
        description += f"{label} at location {bbox}. "
    return description
def get_vqa_answer(image_description, question):
    print(image_description)
    print(question)
    prompt = f"For the given Image Description: {image_description}\n please answer the following Question: {question}\n Answer:"
    client = TavilyClient(api_key=os.getenv('TRAVILY_SECRET_KEY'))
    response = client.qna_search(query=prompt)
    return response
def retinaTavily_vqa(image_path, question):
    detected_objects = detect_objects(image_path)
    image_description = preprocess_detection_results(detected_objects)
    answer = get_vqa_answer(image_description, question)
    return answer 