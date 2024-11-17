from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(255), nullable=False)
