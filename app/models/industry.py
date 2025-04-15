from ..extensions import db

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    def __repr__(self):
        return f'<Industry {self.name}>'
    
    