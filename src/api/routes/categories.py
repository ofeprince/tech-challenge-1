from flask import Blueprint, jsonify, request
from src.models import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories_bp.route('/', methods=['GET'])
def get_categories():
    """
    Return list of categories
    --- 
    responses:
        200:
            description: List of categories
            schema:
                type: array
                items:
                    type: string
    """
    categories = Category.query.all()
    
    result = [ 
        {
            "id": category.id,
            "name": category.name
        } 
        for category in categories 
    ]


    return jsonify(result), 200
