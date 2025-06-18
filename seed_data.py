from database import db_manager
from datetime import datetime

def seed_sample_data():
    """Seed the database with sample product data and view templates"""
    
    # Sample product data with section-based structure
    sample_product = {
        "name": "Premium Auto Oil Filter Pro",
        "structure": [
            {
                "title": "Basic Information",
                "attributes": [
                    {"name": "Product Name", "value": "Premium Auto Oil Filter Pro"},
                    {"name": "SKU", "value": "AOF-PRO-2024-001"},
                    {"name": "Brand", "value": "Advance Auto Parts", "options": ["Advance Auto Parts", "Bosch", "K&N", "Fram", "Mobil 1", "Purolator", "WIX", "AC Delco"]},
                    {"name": "Category", "value": "Automotive Filters", "options": ["Automotive Filters", "Engine Parts", "Maintenance Items", "Performance Parts", "OEM Parts"]},
                    {"name": "Product Type", "value": "Oil Filter", "options": ["Oil Filter", "Air Filter", "Fuel Filter", "Cabin Filter", "Transmission Filter"]},
                    {"name": "Status", "value": "Active", "options": ["Active", "Inactive", "Discontinued", "Coming Soon", "Out of Stock"]},
                    {"name": "Launch Date", "value": "2024-01-15"},
                    {"name": "Discontinue Date", "value": None}
                ]
            },
            {
                "title": "Pricing & Inventory",
                "attributes": [
                    {"name": "Cost Price", "value": "12.50"},
                    {"name": "Selling Price", "value": "24.99"},
                    {"name": "MSRP", "value": "29.99"},
                    {"name": "Currency", "value": "USD", "options": ["USD", "EUR", "GBP", "CAD", "AUD"]},
                    {"name": "Stock Quantity", "value": "150"},
                    {"name": "Minimum Stock Level", "value": "25"},
                    {"name": "Is Trackable", "value": True},
                    {"name": "Backorder Allowed", "value": None}
                ]
            },
            {
                "title": "Physical Specifications",
                "attributes": [
                    {"name": "Weight (lbs)", "value": "0.8"},
                    {"name": "Length (inches)", "value": "4.5"},
                    {"name": "Width (inches)", "value": "3.2"},
                    {"name": "Height (inches)", "value": "3.2"},
                    {"name": "Color", "value": "Black", "options": ["Black", "White", "Silver", "Blue", "Red", "Yellow", "Green"]},
                    {"name": "Material", "value": "Metal", "options": ["Metal", "Plastic", "Composite", "Rubber", "Synthetic", "Paper"]},
                    {"name": "Package Type", "value": "Retail Box", "options": ["Retail Box", "Bulk Pack", "Blister Pack", "Poly Bag", "Custom Packaging"]}
                ]
            },
            {
                "title": "Descriptions & Content",
                "attributes": [
                    {"name": "Short Description", "value": "High-performance oil filter designed for maximum engine protection and extended service life."},
                    {"name": "Long Description", "value": "The Premium Auto Oil Filter Pro features advanced filtration technology with synthetic media that captures 99% of harmful contaminants. Engineered for superior durability and performance, this filter provides exceptional protection for your engine while maintaining optimal oil flow. Perfect for both conventional and synthetic oils."},
                    {"name": "Features", "value": "• Advanced synthetic filtration media\n• 99% contaminant capture efficiency\n• Anti-drainback valve prevents dry starts\n• Silicone gasket for secure seal\n• Heavy-duty steel construction"},
                    {"name": "Benefits", "value": "• Extended engine life\n• Improved fuel economy\n• Reduced maintenance costs\n• Enhanced engine performance\n• Peace of mind protection"},
                    {"name": "Usage Instructions", "value": "1. Ensure engine is cool before installation\n2. Remove old filter using proper filter wrench\n3. Clean filter mounting surface\n4. Apply thin layer of oil to new filter gasket\n5. Install new filter hand-tight plus 3/4 turn\n6. Check for leaks after engine warm-up"},
                    {"name": "Keywords", "value": "oil filter, automotive, engine protection, synthetic media, premium quality"}
                ]
            },
            {
                "title": "Media & Assets",
                "attributes": [
                    {"name": "Primary Image URL", "value": "https://example.com/images/oil-filter-primary.jpg"},
                    {"name": "Gallery Images", "value": "https://example.com/images/oil-filter-1.jpg, https://example.com/images/oil-filter-2.jpg"},
                    {"name": "Video URL", "value": "https://example.com/videos/installation-guide.mp4"},
                    {"name": "Brochure URL", "value": "https://example.com/brochures/oil-filter-specs.pdf"},
                    {"name": "Manual URL", "value": "https://example.com/manuals/installation-manual.pdf"}
                ]
            },
            {
                "title": "Warranty & Support",
                "attributes": [
                    {"name": "Warranty Period (months)", "value": "12"},
                    {"name": "Warranty Type", "value": "Limited", "options": ["Limited", "Full", "Extended", "Lifetime", "No Warranty"]},
                    {"name": "Warranty Coverage", "value": "Covers manufacturing defects and material failures under normal use conditions."},
                    {"name": "Support Contact", "value": "support@advanceautoparts.com"},
                    {"name": "Return Policy", "value": "30-day return policy for unused products in original packaging."}
                ]
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Complete Product View Template
    complete_view_template = {
        "name": "Complete Product View",
        "description": "Comprehensive view with all product details for internal management",
        "is_default": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "sections": [
            {
                "id": "basic-info",
                "title": "Basic Information",
                "order": 0,
                "attributes": [
                    {"id": "1", "name": "Product Name", "type": "String", "required": True},
                    {"id": "2", "name": "SKU", "type": "String", "required": True},
                    {
                        "id": "3",
                        "name": "Brand",
                        "type": "Picklist",
                        "required": True,
                        "options": ["Advance Auto Parts", "Bosch", "K&N", "Fram", "Mobil 1", "Purolator", "WIX", "AC Delco"]
                    },
                    {
                        "id": "4",
                        "name": "Category",
                        "type": "Picklist",
                        "required": True,
                        "options": ["Automotive Filters", "Engine Parts", "Maintenance Items", "Performance Parts", "OEM Parts"]
                    },
                    {
                        "id": "5",
                        "name": "Product Type",
                        "type": "Picklist",
                        "required": True,
                        "options": ["Oil Filter", "Air Filter", "Fuel Filter", "Cabin Filter", "Transmission Filter"]
                    },
                    {
                        "id": "6",
                        "name": "Status",
                        "type": "Picklist",
                        "required": True,
                        "options": ["Active", "Inactive", "Discontinued", "Coming Soon", "Out of Stock"]
                    },
                    {"id": "7", "name": "Launch Date", "type": "Date", "required": False},
                    {"id": "8", "name": "Discontinue Date", "type": "Date", "required": False}
                ]
            },
            {
                "id": "pricing-inventory",
                "title": "Pricing & Inventory",
                "order": 1,
                "attributes": [
                    {"id": "9", "name": "Cost Price", "type": "Number", "required": True},
                    {"id": "10", "name": "Selling Price", "type": "Number", "required": True},
                    {"id": "11", "name": "MSRP", "type": "Number", "required": False},
                    {
                        "id": "12",
                        "name": "Currency",
                        "type": "Picklist",
                        "required": True,
                        "options": ["USD", "EUR", "GBP", "CAD", "AUD"]
                    },
                    {"id": "13", "name": "Stock Quantity", "type": "Number", "required": True},
                    {"id": "14", "name": "Minimum Stock Level", "type": "Number", "required": False},
                    {"id": "15", "name": "Is Trackable", "type": "Boolean", "required": False},
                    {"id": "16", "name": "Backorder Allowed", "type": "Boolean", "required": False}
                ]
            },
            {
                "id": "physical-specs",
                "title": "Physical Specifications",
                "order": 2,
                "attributes": [
                    {"id": "17", "name": "Weight (lbs)", "type": "Number", "required": False},
                    {"id": "18", "name": "Length (inches)", "type": "Number", "required": False},
                    {"id": "19", "name": "Width (inches)", "type": "Number", "required": False},
                    {"id": "20", "name": "Height (inches)", "type": "Number", "required": False},
                    {
                        "id": "21",
                        "name": "Color",
                        "type": "Picklist",
                        "required": False,
                        "options": ["Black", "White", "Silver", "Blue", "Red", "Yellow", "Green"]
                    },
                    {
                        "id": "22",
                        "name": "Material",
                        "type": "Picklist",
                        "required": False,
                        "options": ["Metal", "Plastic", "Composite", "Rubber", "Synthetic", "Paper"]
                    },
                    {
                        "id": "23",
                        "name": "Package Type",
                        "type": "Picklist",
                        "required": False,
                        "options": ["Retail Box", "Bulk Pack", "Blister Pack", "Poly Bag", "Custom Packaging"]
                    }
                ]
            },
            {
                "id": "descriptions",
                "title": "Descriptions & Content",
                "order": 3,
                "attributes": [
                    {"id": "24", "name": "Short Description", "type": "Text", "required": True},
                    {"id": "25", "name": "Long Description", "type": "Rich Text", "required": False},
                    {"id": "26", "name": "Features", "type": "Rich Text", "required": False},
                    {"id": "27", "name": "Benefits", "type": "Rich Text", "required": False},
                    {"id": "28", "name": "Usage Instructions", "type": "Rich Text", "required": False},
                    {"id": "29", "name": "Keywords", "type": "Text", "required": False}
                ]
            },
            {
                "id": "media",
                "title": "Media & Assets",
                "order": 4,
                "attributes": [
                    {"id": "30", "name": "Primary Image URL", "type": "String", "required": True},
                    {"id": "31", "name": "Gallery Images", "type": "Text", "required": False},
                    {"id": "32", "name": "Video URL", "type": "String", "required": False},
                    {"id": "33", "name": "Brochure URL", "type": "String", "required": False},
                    {"id": "34", "name": "Manual URL", "type": "String", "required": False}
                ]
            },
            {
                "id": "warranty-support",
                "title": "Warranty & Support",
                "order": 5,
                "attributes": [
                    {"id": "35", "name": "Warranty Period (months)", "type": "Number", "required": False},
                    {
                        "id": "36",
                        "name": "Warranty Type",
                        "type": "Picklist",
                        "required": False,
                        "options": ["Limited", "Full", "Extended", "Lifetime", "No Warranty"]
                    },
                    {"id": "37", "name": "Warranty Coverage", "type": "Rich Text", "required": False},
                    {"id": "38", "name": "Support Contact", "type": "String", "required": False},
                    {"id": "39", "name": "Return Policy", "type": "Rich Text", "required": False}
                ]
            }
        ]
    }
    
    try:
        # Insert view template first
        view_result = db_manager.view_templates.insert_one(complete_view_template)
        print(f"View template inserted with ID: {view_result.inserted_id}")
        
        # Insert sample product
        product_result = db_manager.products.insert_one(sample_product)
        print(f"Sample product inserted with ID: {product_result.inserted_id}")

        
        result = db_manager.products.insert_many(sample_product)
        
        print("Sample data seeded successfully!")
        print("View template: Complete Product View (default)")
        
    except Exception as e:
        print(f"Error seeding sample data: {e}")

if __name__ == "__main__":
    
    # Then seed sample products and view templates
    seed_sample_data()