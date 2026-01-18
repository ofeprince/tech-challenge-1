from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.api.config import Config
from src.api.extensions import db, swagger, jwt
from src.models import Book, Category, User

app = Flask(__name__)
app.config.from_object(Config)

def add_admin_user():
    user_admin = app.config['ADMIN_USER']
    pass_admin = app.config['PASS_ADMIN']
    
    if User.query.filter_by(username = user_admin).first():
        return jsonify({'Error': 'User already exists'}), 400
    else:
        new_user = User(username = user_admin, password = pass_admin)
        db.session.add(new_user)
        db.session.commit()

# database
db.init_app(app)
with app.app_context():
    db.create_all()
    add_admin_user()

# JWT
jwt.init_app(app)

# /apidocs/
swagger.init_app(app)

@app.route('/')
def home():
    return "Hello, world!"


# Afterward, change it for a database
list_test = [
    "Book 1",
    "Book 2"
]

# Get books from database
@app.route('/api/v1/books', methods=['GET'])
def get_books():
    """
    Retorna lista de livros
    --- 
    responses:
        200:
            description: Lista de livros disponíveis
            schema:
                type: array
                items:
                    type: string
    """
    
    return jsonify(list_test)

# Here define def by query
# TODO
@app.route('/api/v1/books_to_implement_with_query', methods=['GET'])
def get_books_by_query_options():
    return jsonify(list_test), 200

# Get book by ID
@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    return jsonify(list_test[book_id])


@app.route('/api/v1/categories', methods=['GET'])
def get_categories():
    return jsonify(['cat 1', 'cat2'])

# Health
# TODO
@app.route('/api/v1/health', methods=['GET'])
def get_health():
    return jsonify(['OK']), 200

# Auth
# TODO - Retornar token
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    user_dto = request.get_json()
    found_user = User.query.filter_by(username = user_dto['username']).first()
    if found_user and found_user.password == user_dto['password']:
        token = create_access_token(identity=str(found_user.id))
        return jsonify({'access_token': token}), 200
    
    return jsonify({'Error': 'Invalid credentials'}), 401

# Refresh token
# TODO
@app.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    return 200

# Scrape
# TODO
@app.route('/api/v1/scraping/execute', methods=['POST'])
@jwt_required()
def scrape():
    """
    Extract data from the website to the database
    ---
    responses:
        200:
            description: Scrape has been executed successfully.
    """
    # Start the extraction
    # Save the result with category and books into the database
    # Return success

    return jsonify({'Message': 'Ok'}), 200

if __name__ == '__main__':
    app.run(debug = True)