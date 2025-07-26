from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo 
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MyApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.configure_app()
        self.asset_url = '/static/jc.css'
        self.setup_routes()

    def configure_app(self):
        # Configure MongoDB connection
        mongodb_uri = os.getenv('MONGODB_URI')
        print(f'MONGODB_URI: {mongodb_uri}')  # Debugging line
        self.app.config["MONGO_URI"] = mongodb_uri
        self.mongo = PyMongo(self.app)

    def get_metadata_by_page(self, page):
        collection_name = os.getenv('COLLECTION_NAME')
        if collection_name is None:
            raise ValueError("COLLECTION_NAME environment variable is not set.")
        
        print(f'Accessing collection: {collection_name}')  # Debugging line
        collection = self.mongo.db[collection_name]
        
        if not isinstance(collection, str):  # Check if collection is a valid object
            return collection.find_one({'page': page}, {'_id': 0, 'page': 1, 'title': 1, 'keywords': 1, 'description': 1})
        else:
            raise ValueError(f"Expected a collection object but got: {type(collection)}")

    def setup_routes(self):
        @self.app.route('/')
        def home():
            # Call the general method to get metadata for the "home" page
            document = self.get_metadata_by_page('home')
            
            # Prepare the SEO data for rendering
            home_seo = {
                'title': document.get('title', ''),  # Fallback to a default title if not found
                'description': document.get('description', '.'),
                'keywords': document.get('keywords', ''),
            }
            return render_template('index.html', seo=home_seo)

    def run(self):
        self.app.run(debug=True)
        
if __name__ == '__main__':
    app_instance = MyApp()
    app_instance.run()