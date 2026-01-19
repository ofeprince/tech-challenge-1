from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)
from sqlalchemy import text 
from src.api.config import Config
from src.api.extensions import db, swagger, jwt
from src.models import Book, Category, User
from src.shared import (
    get_categories as scrape_categories,
    scrape_category
)

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
    books = Book.query.all() # retorna lista de objetos Book
    # transformar em JSON
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


@app.route('/api/v1/books/search', methods=['GET'])
def get_books_by_query_options():
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

# Get book by ID
@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
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

# Get categories from database
@app.route('/api/v1/categories', methods=['GET'])
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

# Health
@app.route('/api/v1/health', methods=['GET'])
def get_health():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 500
  
# Auth
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    user_dto = request.get_json()
    found_user = User.query.filter_by(username = user_dto['username']).first()
    if found_user and found_user.password == user_dto['password']:
        token = create_access_token(identity = str(found_user.id))
        refresh_token = create_refresh_token(identity = str(found_user.id))
        return jsonify({'access_token': token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'Error': 'Invalid credentials'}), 401

# Refresh token
@app.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity = identity)
    return jsonify(access_token=access_token)

# Scrape
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

    # 0. Obter dados raspados
    books_data = []
    categories = scrape_categories()
    for category_name, category_url in categories.items():
        print(f"Scraping category: {category_name}")
        books_data.extend(scrape_category(category_name, category_url))

    # 1. Extrair categorias únicas
    category_names = {book["category"] for book in books_data}

    # 2. Buscar categorias já existentes
    existing_categories = db.session.query(Category).filter(Category.name.in_(category_names)).all()
    category_map = {c.name: c.id for c in existing_categories}

    # 3. Criar categorias novas
    new_categories = []
    for name in category_names:
        if name not in category_map:
            new_categories.append(Category(name=name))

    db.session.add_all(new_categories)
    db.session.flush()  # gera IDs para novas categorias

    # Atualizar o mapa com as novas categorias
    for c in new_categories:
        category_map[c.name] = c.id

    # 4. Criar livros
    new_books = []
    for book_data in books_data:
        book = Book(
            title = book_data["title"],
            category_id = category_map[book_data["category"]],
            price = book_data["price"],
            rating = book_data["rating"],
            availability = book_data["availability"],
            image_src = book_data["image_src"]
        )
        new_books.append(book)

    db.session.add_all(new_books)

    # 5. Commit único
    db.session.commit()

    return jsonify({'Message': 'Ok'}), 200

if __name__ == '__main__':
    app.run(debug = True)