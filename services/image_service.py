import json
import os
from flask import make_response
from models.vilt_model import calling_vilt_pipeline
from models.vqa_model import VQAModel
from models.retina_tavily import retinaTavily_vqa
import chromadb
import pickle
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
        return make_response({'message': str(e)}, 500)
    

def image_search_vilt(requestData):
    try:
        if 'image' not in requestData.files or 'question' not in requestData.form:
            return make_response({"error": "Missing image or question"}, 400)
        image = requestData.files['image']
        question = requestData.form['question']
        image_path = f"temp_{image.filename}"
        image.save(image_path)

        answer = calling_vilt_pipeline(image_path, question)
        json_string = json.dumps(answer, indent=4)
        # Store result in ChromaDB
        collection.add(
            documents=[json_string],
            metadatas=[{"question": question, "image_name": image.filename}],
            ids=[f"{image.filename}_{question}"]
        )
        # Generate and store the pickle file 
        with open('model_output.pickle', 'wb') as file:
            pickle.dump(answer, file)

        os.remove(image_path)
        return make_response({'result':answer[0]})
    except Exception as e:
        return make_response({'message': str(e)}, 500)
    

def image_search_retina(requestData):
    try:
        if 'image' not in requestData.files or 'question' not in requestData.form:
            return make_response({"error": "Missing image or question"}, 400)
        image = requestData.files['image']
        question = requestData.form['question']
        image_path = f"temp_{image.filename}"
        image.save(image_path)
        print(image)
        answer = retinaTavily_vqa(image_path, question)
        os.remove(image_path)
        return make_response({'result':answer})
    except Exception as e:
        return make_response({'message': str(e)}, 500)