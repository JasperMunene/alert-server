# blogs_resource.py
from flask_restful import Resource, reqparse
from flask import request, jsonify
from models import db, Post, User, Tag
from datetime import datetime
import uuid
from slugify import slugify

# Request parser for creating posts
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, help='Title is required')
post_parser.add_argument('body', type=str, required=True, help='Body content is required')
post_parser.add_argument('excerpt', type=str, required=False)
post_parser.add_argument('status', type=str, required=False, default='draft')
post_parser.add_argument('cover_image', type=str, required=False)
post_parser.add_argument('author_id', type=str, required=True, help='Author ID is required')
post_parser.add_argument('tags', type=str, action='append', required=False)
post_parser.add_argument('slug', type=str, required=False)

class BlogPosts(Resource):
    def get(self, post_id=None):
        """Get all posts or a specific post by ID"""
        if post_id:
            # Get a specific post
            post = Post.query.get_or_404(post_id)
            return jsonify(post.to_dict())
        else:
            # Get all posts with optional filtering
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            status = request.args.get('status', None)
            author_id = request.args.get('author_id', None)
            tag = request.args.get('tag', None)
            
            query = Post.query
            
            if status:
                query = query.filter(Post.status == status)
            if author_id:
                query = query.filter(Post.author_id == author_id)
            if tag:
                query = query.join(Post.tags).filter(Tag.name == tag)
            
            posts = query.order_by(Post.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'posts': [post.to_dict() for post in posts.items],
                'total': posts.total,
                'pages': posts.pages,
                'current_page': page
            })
    
    def post(self):
        """Create a new blog post"""
        try:
            args = post_parser.parse_args()
            
            # Validate author exists
            author = User.query.get(args['author_id'])
            if not author:
                return {'message': 'Author not found'}, 404
            
            # Generate slug if not provided
            slug = args.get('slug')
            if not slug:
                slug = slugify(str(args['title'])) 
            
            # Check if slug already exists
            if Post.query.filter_by(slug=slug).first():
                return {'message': 'Slug already exists'}, 409
            
            # Create the post
            post = Post(
                title=args['title'],
                slug=slug,
                excerpt=args.get('excerpt', ''),
                body=args['body'],
                status=args['status'],
                cover_image=args.get('cover_image', ''),
                author_id=args['author_id']
            )
            
            # Set published_at if status is published
            if args['status'] == 'published':
                post.published_at = datetime.utcnow()
            
            # Handle tags
            if args.get('tags'):
                for tag_name in args['tags']:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        # Create new tag if it doesn't exist
                        tag_slug = slugify(tag_name)
                        tag = Tag(name=tag_name, slug=tag_slug)
                        db.session.add(tag)
                    post.tags.append(tag)
            
            db.session.add(post)
            db.session.commit()
            
            return post.to_dict(), 201
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating post: {str(e)}'}, 500
    
    def put(self, post_id):
        """Update an existing blog post"""
        try:
            post = Post.query.get_or_404(post_id)
            args = post_parser.parse_args()
            
            # Update fields
            if 'title' in args and args['title']:
                post.title = args['title']
            
            if 'body' in args and args['body']:
                post.body = args['body']
            
            if 'excerpt' in args:
                post.excerpt = args['excerpt']
            
            if 'status' in args and args['status']:
                post.status = args['status']
                # Update published_at if status changed to published
                if args['status'] == 'published' and not post.published_at:
                    post.published_at = datetime.utcnow()
            
            if 'cover_image' in args:
                post.cover_image = args['cover_image']
            
            # Handle tags if provided
            if 'tags' in args and args['tags'] is not None:
                post.tags = []
                for tag_name in args['tags']:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if not tag:
                        # Create new tag if it doesn't exist
                        tag_slug = slugify(tag_name)
                        tag = Tag(name=tag_name, slug=tag_slug)
                        db.session.add(tag)
                    post.tags.append(tag)
            
            db.session.commit()
            
            return post.to_dict()
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating post: {str(e)}'}, 500
    
    def delete(self, post_id):
        """Delete a blog post"""
        try:
            post = Post.query.get_or_404(post_id)
            db.session.delete(post)
            db.session.commit()
            
            return {'message': 'Post deleted successfully'}, 200
            
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting post: {str(e)}'}, 500

class BlogPostBySlug(Resource):
    def get(self, slug):
        """Get a post by its slug"""
        post = Post.query.filter_by(slug=slug).first_or_404()
        return jsonify(post.to_dict())