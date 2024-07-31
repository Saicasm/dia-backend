
from flask import Blueprint, request
from services.image_service import image_search, image_search_vilt
image_route = Blueprint('image_route', __name__)

@DeprecationWarning
@image_route.route("/api/v1/image/vqa", methods=['POST'])
def image():
    return image_search(request)
@image_route.route("/api/v1/image/vilt", methods=['POST'])
def image_vilt():
    return image_search_vilt(request)
    