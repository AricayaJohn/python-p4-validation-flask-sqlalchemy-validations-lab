from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        elif Author.query.filter_by(name = name).first():
            raise ValueError("Name must be unique")
        return name

    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be equal to 10 digits")
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only numbers")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('content', 'summary')
    def validate_content(self, key, string):
        if (key == 'content'):
            if len(string) < 250:
                raise ValueError("Content must be greater than or equal to 250 characters.")
        if (key == 'summary'):
            if len(string) > 250:
                raise ValueError("Summary must be less than or equal to 250 characters.")
        return string

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
