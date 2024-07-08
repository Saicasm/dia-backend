from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image

class VQAModel:
    def __init__(self):
        self.processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    def answer_question(self, image_path, question):
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, question, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        return self.model.config.id2label[idx]