# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData, event
from sqlalchemy.orm import validates
import uuid
from datetime import datetime
import re
from slugify import slugify 

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    
    serialize_rules = ('-posts.author', '-password_hash')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Tag(db.Model, SerializerMixin):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    
    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')
    
    serialize_rules = ('-posts.tags',)
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Tag name cannot be empty")
        if len(name) > 80:
            raise ValueError("Tag name cannot exceed 80 characters")
        return name.strip()
    
    @validates('slug')
    def validate_slug(self, key, slug):
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
            raise ValueError("Slug can only contain lowercase letters, numbers, and hyphens")
        return slug
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(300), nullable=False, index=True)
    slug = db.Column(db.String(320), nullable=False, unique=True, index=True)
    excerpt = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='draft')
    cover_image = db.Column(db.String(1024), nullable=True)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    views = db.Column(db.Integer, default=0, nullable=False)
    
    tags = db.relationship('Tag', secondary='post_tags', back_populates='posts')
    
    serialize_rules = ('-author.posts', '-tags.posts')
    
    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 300:
            raise ValueError("Title cannot exceed 300 characters")
        return title.strip()
    
    @validates('slug')
    def validate_slug(self, key, slug):
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
            raise ValueError("Slug can only contain lowercase letters, numbers, and hyphens")
        return slug
    
    @validates('status')
    def validate_status(self, key, status):
        if status not in ['draft', 'published', 'archived']:
            raise ValueError("Status must be either 'draft', 'published', or 'archived'")
        return status
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Association table
post_tags = db.Table('post_tags',
    db.Column('post_id', db.String(36), db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

# Event listener to update the updated_at timestamp automatically
@event.listens_for(Post, 'before_update')
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()

@event.listens_for(User, 'before_update')
def update_user_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()