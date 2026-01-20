from flask import Flask, jsonify
from sqlalchemy import text 
from src.api.config import Config
from src.api.extensions import db, swagger, jwt
from src.models import User
from src.api.routes import (
    categories_bp, books_bp, auth_bp, scraping_bp
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

# Controllers blueprint
app.register_blueprint(categories_bp)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(scraping_bp)

@app.route('/api/v1/health', methods=['GET'])
def get_health():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 500
  
if __name__ == '__main__':
    app.run(debug = True)