from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client.product_management  # Access 'product_management' database

# Define MongoDB collections
products_collection = db.products
view_templates_collection = db.view_templates

# Helper function to convert ObjectId to string for JSON serialization
def serialize_doc(doc):
    if doc and '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def serialize_docs(docs):
    return [serialize_doc(doc) for doc in docs]

# ---------------------------- Product Routes ----------------------------

# Get all products
@app.route('/productManagement/get-products', methods=['GET'])
def get_products():
    try:
        products = list(products_collection.find())
        return jsonify(serialize_docs(products))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single product by ID
@app.route('/productManagement/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(serialize_doc(product))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new product
@app.route('/productManagement/create-product', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = products_collection.insert_one(data)
        # product = products_collection.find_one({'_id': result.inserted_id})
        return jsonify({'Success': "Product is Created Successfully"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing product by ID (converted to POST)
@app.route('/productManagement/update-product/<product_id>', methods=['POST'])
def update_product(product_id):
    try:
        data = request.get_json()
        data['updated_at'] = datetime.utcnow()
        result = products_collection.update_one({'_id': ObjectId(product_id)}, {'$set': data})
        if result.matched_count == 0:
            return jsonify({'error': 'Product not found'}), 404
        product = products_collection.find_one({'_id': ObjectId(product_id)})
        return jsonify(serialize_doc(product))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a product by ID (converted to POST)
@app.route('/productManagement/delete-product/<product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        result = products_collection.delete_one({'_id': ObjectId(product_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------ View Template Routes ------------------------

# Get all view templates
@app.route('/productManagement/view-templates', methods=['GET'])
def get_view_templates():
    try:
        templates = list(view_templates_collection.find())
        return jsonify(serialize_docs(templates))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a single view template by ID
@app.route('/productManagement/view-template/<template_id>', methods=['GET'])
def get_view_template(template_id):
    try:
        template = view_templates_collection.find_one({'_id': ObjectId(template_id)})
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify(serialize_doc(template))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new view template
@app.route('/productManagement/create-view', methods=['POST'])
def create_view_template():
    try:
        data = request.get_json()
        data['created_at'] = datetime.utcnow().strftime('%Y-%m-%d')
        data['last_modified'] = datetime.utcnow().strftime('%Y-%m-%d')
        result = view_templates_collection.insert_one(data)
        template = view_templates_collection.find_one({'_id': result.inserted_id})
        return jsonify(serialize_doc(template)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing view template (converted to POST)
@app.route('/productManagement/update-view/<template_id>', methods=['POST'])
def update_view_template(template_id):
    try:
        data = request.get_json()
        data['last_modified'] = datetime.utcnow().strftime('%Y-%m-%d')
        result = view_templates_collection.update_one({'_id': ObjectId(template_id)}, {'$set': data})
        if result.matched_count == 0:
            return jsonify({'error': 'Template not found'}), 404
        template = view_templates_collection.find_one({'_id': ObjectId(template_id)})
        return jsonify(serialize_doc(template))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a view template (converted to POST)
@app.route('/productManagement/delete-view/<template_id>', methods=['POST'])
def delete_view_template(template_id):
    try:
        template = view_templates_collection.find_one({'_id': ObjectId(template_id)})
        if template and template.get('is_default'):
            return jsonify({'error': 'Cannot delete default template'}), 400
        result = view_templates_collection.delete_one({'_id': ObjectId(template_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Template not found'}), 404
        return jsonify({'message': 'Template deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------ Health Check ------------------------

# Simple health check endpoint
@app.route('/productManagement/health', methods=['GET'])
def health_check():
    try:
        db.command('ping')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# Start the Flask application
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)