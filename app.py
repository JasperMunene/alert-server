from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from dotenv import load_dotenv
from resources.blogs_resource import BlogPosts, BlogPostBySlug
import os

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("CONNECTION_STRING")

db.init_app(app)


migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Define a HealthCheck Resource
class HealthCheck(Resource):
    def get(self):
        return {'status': 'OK'},

# Add resource to API
api.add_resource(HealthCheck, '/api/v1/health')
api.add_resource(BlogPosts, '/api/v1/posts', '/api/v1/posts/<string:post_id>')
api.add_resource(BlogPostBySlug, '/api/v1/posts/slug/<string:slug>')

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)