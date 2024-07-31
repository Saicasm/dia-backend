import os
from flask import Flask, request, jsonify
from models.vqa_model import VQAModel
from flask_cors import CORS
from api.image import image_route
app = Flask(__name__)
app.register_blueprint(image_route)
CORS(app)

secret_key = os.getenv('SECRET_KEY')

app.config['SECRET_KEY'] = secret_key

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)