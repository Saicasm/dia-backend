import os
from flask import make_response
from models.vqa_model import VQAModel
import chromadb
vqa_model = VQAModel()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="vqa_results")
def image_search(requestData):
    try:
        if 'image' not in requestData.files or 'question' not in requestData.form:
            return make_response({"error": "Missing image or question"}, 400)
        image = requestData.files['image']
        question = requestData.form['question']
        image_path = f"temp_{image.filename}"
        image.save(image_path)

        answer = vqa_model.answer_question(image_path, question)

        # Store result in ChromaDB
        collection.add(
            documents=[answer],
            metadatas=[{"question": question, "image_name": image.filename}],
            ids=[f"{image.filename}_{question}"]
        )

        os.remove(image_path)
        return make_response({'answer':answer})
    except Exception as e:
        return make_response({'message': str(e)}, 404)
    

    