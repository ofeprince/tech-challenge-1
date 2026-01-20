from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.api.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from src.models import Book, Category
from src.shared import (
    get_categories as scrape_categories,
    scrape_category
)

scraping_bp = Blueprint('scraping', __name__, url_prefix='/api/v1/scraping')

@scraping_bp.route('/execute', methods=['POST'])
@jwt_required()
def scrape():
    """
    Extract data from the website to the database
    ---
    security:
        - Bearer: []
    responses:
        200:
            description: Scraping has been executed successfully.
        500:
            description: An error occurred during scraping or data operation.
    """
    try:
        books_data = []
        categories = scrape_categories()
        for category_name, category_url in categories.items():
            print(f"Scraping category: {category_name}")
            books_data.extend(scrape_category(category_name, category_url))
            
        category_names = {book["category"] for book in books_data}
        
        existing_categories = db.session.query(Category).filter(Category.name.in_(category_names)).all()
        category_map = {c.name: c.id for c in existing_categories}
        
        new_categories = []
        for name in category_names:
            if name not in category_map:
                new_categories.append(Category(name=name))

        db.session.add_all(new_categories)
        db.session.flush()
        
        for c in new_categories:
            category_map[c.name] = c.id
            
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
        db.session.commit()

        return jsonify({'Message': 'Scraping executed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'Error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'Error': 'Scraping error', 'details': str(e)}), 500
