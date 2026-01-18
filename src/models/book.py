from src.api.extensions import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    preco = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    disponibilidade = db.Column(db.String)
    imagem_url = db.Column(db.String)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("Category", back_populates="books")