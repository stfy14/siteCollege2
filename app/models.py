from app import db
from datetime import datetime

class Work(db.Model):
    __tablename__ = 'works'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    award = db.Column(db.String(50))
    university = db.Column(db.String(100))
    direction = db.Column(db.String(100))
    file_path = db.Column(db.String(200))  # Обычно хранится только имя файла
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Work {self.title}>'
