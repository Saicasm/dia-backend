
from flask import Blueprint, request
from services.image_service import image_search
image_route = Blueprint('image_route', __name__)

@image_route.route("/api/v1/image/vqa", methods=['POST'])
def image():

    return image_search(request)


# @image_route.route('"/api/v1/image/search', methods=['GET'])
# def search_results():
#     query = request.args.get('query', '')
#     results = collection.query(query_texts=[query], n_results=5)
#     return jsonify(results)
