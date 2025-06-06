from bson import ObjectId
from datetime import datetime
import re

def serialize_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if key == '_id' and isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                serialized[key] = serialize_doc(value)
            else:
                serialized[key] = value
        return serialized
    
    return doc

def validate_product_data(data):
    """Validate product data before saving"""
    errors = []
    
    # Required fields validation
    required_fields = ['product_name', 'sku']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")
    
    # SKU format validation (alphanumeric with hyphens)
    sku = data.get('sku', '')
    if sku and not re.match(r'^[A-Za-z0-9\-_]+$', sku):
        errors.append("SKU must contain only letters, numbers, hyphens, and underscores")
    
    # Price validation
    for price_field in ['cost_price', 'selling_price', 'msrp']:
        if price_field in data:
            try:
                price = float(data[price_field])
                if price < 0:
                    errors.append(f"{price_field} must be non-negative")
            except (ValueError, TypeError):
                errors.append(f"{price_field} must be a valid number")
    
    # Stock quantity validation
    if 'stock_quantity' in data:
        try:
            stock = int(data['stock_quantity'])
            if stock < 0:
                errors.append("Stock quantity must be non-negative")
        except (ValueError, TypeError):
            errors.append("Stock quantity must be a valid integer")
    
    return errors

def validate_view_template(template_data):
    """Validate view template data"""
    errors = []
    
    # Required fields
    if not template_data.get('name'):
        errors.append("Template name is required")
    
    if not template_data.get('description'):
        errors.append("Template description is required")
    
    # Sections validation
    sections = template_data.get('sections', [])
    if not sections:
        errors.append("Template must have at least one section")
    
    for i, section in enumerate(sections):
        if not section.get('title'):
            errors.append(f"Section {i+1} must have a title")
        
        if not isinstance(section.get('order'), int):
            errors.append(f"Section {i+1} must have a valid order number")
        
        attributes = section.get('attributes', [])
        for j, attr in enumerate(attributes):
            if not attr.get('name'):
                errors.append(f"Attribute {j+1} in section {i+1} must have a name")
            
            if attr.get('type') not in ['String', 'Number', 'Boolean', 'Date', 'Text', 'Rich Text', 'Picklist']:
                errors.append(f"Attribute {j+1} in section {i+1} has invalid type")
    
    return errors

def build_search_query(search_params):
    """Build MongoDB query from search parameters"""
    query = {}
    
    # Text search
    if search_params.get('q'):
        query['$text'] = {'$search': search_params['q']}
    
    # Category filter
    if search_params.get('category'):
        query['category'] = search_params['category']
    
    # Status filter
    if search_params.get('status'):
        query['status'] = search_params['status']
    
    # Brand filter
    if search_params.get('brand'):
        query['brand'] = search_params['brand']
    
    # Price range filter
    if search_params.get('min_price') or search_params.get('max_price'):
        price_query = {}
        if search_params.get('min_price'):
            price_query['$gte'] = float(search_params['min_price'])
        if search_params.get('max_price'):
            price_query['$lte'] = float(search_params['max_price'])
        query['selling_price'] = price_query
    
    # Date range filter
    if search_params.get('created_after'):
        query['created_at'] = {'$gte': datetime.fromisoformat(search_params['created_after'])}
    
    return query

def generate_sku():
    """Generate a unique SKU"""
    import random
    import string
    
    # Generate random alphanumeric string
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    timestamp_part = datetime.now().strftime('%Y%m')
    
    return f"PRD-{timestamp_part}-{random_part}"

def calculate_product_stats(products):
    """Calculate statistics for products"""
    if not products:
        return {
            'total_products': 0,
            'active_products': 0,
            'total_value': 0,
            'categories': {},
            'brands': {}
        }
    
    stats = {
        'total_products': len(products),
        'active_products': 0,
        'total_value': 0,
        'categories': {},
        'brands': {}
    }
    
    for product in products:
        # Count active products
        if product.get('status') == 'Active':
            stats['active_products'] += 1
        
        # Calculate total value
        selling_price = product.get('selling_price', 0)
        stock_quantity = product.get('stock_quantity', 0)
        try:
            stats['total_value'] += float(selling_price) * int(stock_quantity)
        except (ValueError, TypeError):
            pass
        
        # Count categories
        category = product.get('category')
        if category:
            stats['categories'][category] = stats['categories'].get(category, 0) + 1
        
        # Count brands
        brand = product.get('brand')
        if brand:
            stats['brands'][brand] = stats['brands'].get(brand, 0) + 1
    
    return stats
