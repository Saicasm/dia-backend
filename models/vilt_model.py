
from transformers import pipeline

from PIL import Image

# Add env for model reference
modelref = "dandelin/vilt-b32-finetuned-vqa"
vqa_pipeline = pipeline("visual-question-answering",
                        model=modelref)

vqa_pipeline

def calling_vilt_pipeline(image_path, question):
    """
    Calling the ViLT pipeline
    """
    actual_image=Image.open(image_path).convert("RGB")
    predictions = vqa_pipeline(actual_image, question, top_k=10)
    return predictions,

