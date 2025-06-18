from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Name is required")
        
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author name must be unique")
        
        return name

    @validates("phone_number") 
    def validate_phone_number(self, key, phone_number):
        if not phone_number:
            raise ValueError("Phone number is required")

        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")

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
    @validates("title")
    def validates_title(self, key, title):
        if not title or title.strip() == "":
            raise ValueError("Post title is required")
        
        phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in phrases):
            raise ValueError("Post title must be clickbait-y and contain one of: 'Won't Believe', 'Secret', 'Top', or 'Guess'")

        return title
    
    @validates("content")
    def validates_content(self, key, content):
        if not content :
            raise ValueError("Post Content is required")
        
        if len(content) < 250:
            raise ValueError("Post Content should be atleast 250 characters")

        return content
    
    @validates("summary")
    def validates_summary(self, key, summary):
        if not summary :
            raise ValueError("Post Summary is required")
        
        if len(summary) > 250:
            raise ValueError("Post Summary should be less than 250 characters")

        return summary
    
    @validates("category")
    def validates_category(self, key, category):
        if not category :
            raise ValueError("Post Category is required")
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Invalid Post Category")
        
        return category 
    

        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
