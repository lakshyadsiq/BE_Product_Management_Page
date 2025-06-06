from pymongo import MongoClient
from datetime import datetime
import os
from typing import Optional, Dict, List, Any
from models import Product, ViewTemplate, ProductManager

class DatabaseManager:
    def __init__(self, mongo_uri: Optional[str] = None):
        self.mongo_uri = mongo_uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.product_management
        
        # Collections
        self.products = self.db.products
        self.view_templates = self.db.view_templates
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Product indexes
            self.products.create_index([("sku", 1)], unique=True, sparse=True)
            self.products.create_index([("structure.attributes.name", "text"), ("structure.attributes.value", "text")])
            self.products.create_index([("created_at", -1)])
            
            # View template indexes
            self.view_templates.create_index([("name", 1)])
            self.view_templates.create_index([("is_default", 1)])
            
            print("Database indexes created successfully")
        except Exception as e:
            print(f"Error creating indexes: {e}")
    
    def save_product(self, product: Product) -> bool:
        """Save or update a product in the database"""
        try:
            product_dict = product.to_dict()
            self.products.update_one(
                {"sku": product_dict.get("sku")},
                {"$set": product_dict},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving product: {e}")
            return False
    
    def get_product(self, sku: str) -> Optional[Product]:
        """Retrieve a product by SKU"""
        try:
            product_dict = self.products.find_one({"sku": sku})
            if product_dict:
                return Product(product_dict)
            return None
        except Exception as e:
            print(f"Error retrieving product: {e}")
            return None
    
    def delete_product(self, sku: str) -> bool:
        """Delete a product by SKU"""
        try:
            result = self.products.delete_one({"sku": sku})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def save_view_template(self, view_template: ViewTemplate) -> bool:
        """Save or update a view template in the database"""
        try:
            view_dict = view_template.to_dict()
            self.view_templates.update_one(
                {"id": view_dict["id"]},
                {"$set": view_dict},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving view template: {e}")
            return False
    
    def get_view_template(self, view_id: str) -> Optional[ViewTemplate]:
        """Retrieve a view template by ID"""
        try:
            view_dict = self.view_templates.find_one({"id": view_id})
            if view_dict:
                manager = ProductManager()
                manager.load_from_dict({"view_templates": [view_dict]})
                return manager.get_view_template(view_id)
            return None
        except Exception as e:
            print(f"Error retrieving view template: {e}")
            return None
    
    def delete_view_template(self, view_id: str) -> bool:
        """Delete a view template by ID"""
        try:
            view = self.get_view_template(view_id)
            if view and view.is_default:
                print("Cannot delete default view template")
                return False
            result = self.view_templates.delete_one({"id": view_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting view template: {e}")
            return False
    
    def get_all_products(self) -> List[Product]:
        """Retrieve all products"""
        try:
            products = []
            for product_dict in self.products.find():
                products.append(Product(product_dict))
            return products
        except Exception as e:
            print(f"Error retrieving products: {e}")
            return []
    
    def get_all_view_templates(self) -> List[ViewTemplate]:
        """Retrieve all view templates"""
        try:
            manager = ProductManager()
            view_dicts = list(self.view_templates.find())
            if view_dicts:
                manager.load_from_dict({"view_templates": view_dicts})
            return manager.view_templates
        except Exception as e:
            print(f"Error retrieving view templates: {e}")
            return []
    
    def close_connection(self):
        """Close database connection"""
        self.client.close()

# Initialize database manager
db_manager = DatabaseManager()