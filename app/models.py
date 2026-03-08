from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

    status = db.Column(
        db.Enum('open','in progress', 'completed', name='status_types'),
        default = 'open',
        nullable = False
    )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

