from flask import Blueprint, jsonify, request
from src.models import Book, Category

books_bp = Blueprint('books', __name__, url_prefix='/api/v1/books')

@books_bp.route('/', methods=['GET'])
def get_books():
    """
    Returns list of available books
    --- 
    responses:
        200:
            description: List of books
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                        title:
                            type: string
                        price:
                            type: string
                        rating:
                            type: integer
                        availability:
                            type: string
                        image_src:
                            type: string
                        category_id:
                            type: integer
    """
    books = Book.query.all()
    
    result = [ 
        {
            "id": b.id,
            "title": b.title,
            "price": b.price,
            "rating": b.rating,
            "availability": b.availability,
            "image_src": b.image_src,
            "category_id": b.category_id
        } 
        for b in books 
    ]


    return jsonify(result), 200

@books_bp.route('/search', methods=['GET'])
def get_books_by_query_options():
    """
    Returns books filtered by title or category
    ---
    parameters:
        - in: query
          name: title
          type: string
          required: false
          description: Title of the book to search for
        - in: query
          name: category
          type: string
          required: false
          description: Category name to filter books by
    responses:
        200:
            description: List of books matching the query
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                        title:
                            type: string
                        price:
                            type: string
                        rating:
                            type: integer
                        availability:
                            type: string
                        image_src:
                            type: string
                        category_id:
                            type: integer
    """
    
    title = request.args.get('title')
    category_name = request.args.get('category')

    query = Book.query

    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))

    if category_name:
        query = query.join(Category).filter(Category.name.ilike(f'%{category_name}%'))
    
    books = query.all()
    result = [ 
        {
            "id": b.id,
            "title": b.title,
            "price": b.price,
            "rating": b.rating,
            "availability": b.availability,
            "image_src": b.image_src,
            "category_id": b.category_id
        } 
        for b in books 
    ]

    return jsonify(result), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """
    Returns a book by its ID
    ---
    parameters:
        - in: path
          name: book_id
          type: integer
          required: true
          description: ID of the book to retrieve
    responses:
        200:
            description: Book found
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    title:
                        type: string
                    price:
                        type: string
                    rating:
                        type: integer
                    availability:
                        type: string
                    image_src:
                        type: string
                    category_id:
                        type: integer
    """
    found_book = Book.query.filter_by(id = book_id).first()
    if not found_book:
        return jsonify({'Error': 'Book not found'}), 404
    return jsonify({
        "id": found_book.id,
        "title": found_book.title,
        "price": found_book.price,
        "rating": found_book.rating,
        "availability": found_book.availability,
        "image_src": found_book.image_src,
        "category_id": found_book.category_id
    }), 200
