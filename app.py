from flask import Flask, request, jsonify
from models.vqa_model import VQAModel
import chromadb
from flask_cors import CORS
from api.image import image_route
app = Flask(__name__)
app.register_blueprint(image_route)
CORS(app)

@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('query', '')
    results = collection.query(query_texts=[query], n_results=5)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)