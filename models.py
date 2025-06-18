from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from copy import deepcopy

class ProductAttribute:
    VALID_TYPES = {"String", "Number", "Boolean", "Date", "Text", "Rich Text", "Picklist"}

    def __init__(self, id: Union[int, str], name: str, type: str, required: bool = False, 
                 value: Any = None, options: Optional[List[str]] = None):
        if type not in self.VALID_TYPES:
            raise ValueError(f"Invalid attribute type: {type}. Must be one of {self.VALID_TYPES}")
        self.id = str(id)
        self.name = name
        self.type = type
        self.required = required
        self.value = value
        self.options = options if type == "Picklist" else None

    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'required': self.required
        }
        if self.value is not None:
            result['value'] = self.value
        if self.type == "Picklist" and self.options:
            result['options'] = self.options
        return result

    def validate_value(self, value: Any) -> bool:
        if value is None:
            return not self.required
        if self.type == "String":
            return isinstance(value, str)
        elif self.type == "Number":
            try:
                float(value)
                return True
            except (ValueError, TypeError):
                return False
        elif self.type == "Boolean":
            return isinstance(value, bool) or value is None
        elif self.type == "Date":
            try:
                datetime.strptime(str(value), '%Y-%m-%d')
                return True
            except (ValueError, TypeError):
                return False
        elif self.type in {"Text", "Rich Text"}:
            return isinstance(value, str) or value is None
        elif self.type == "Picklist":
            return isinstance(value, str) and (not self.options or value in self.options)
        return False

    def add_option(self, option: str):
        if self.type == "Picklist" and option and option not in (self.options or []):
            self.options = self.options or []
            self.options.append(option)

    def remove_option(self, option: str):
        if self.type == "Picklist" and self.options and option in self.options:
            self.options.remove(option)

    def reorder_options(self, new_order: List[str]):
        if self.type == "Picklist" and self.options and set(new_order) == set(self.options):
            self.options = new_order
        elif self.type == "Picklist":
            raise ValueError("New order must contain exactly the same options")

class ProductSection:
    def __init__(self, id: str, title: str, order: int, attributes: List[ProductAttribute] = None):
        self.id = id
        self.title = title
        self.order = order
        self.attributes = attributes or []

    def add_attribute(self, attribute: ProductAttribute):
        self.attributes.append(attribute)

    def remove_attribute(self, attribute_id: Union[int, str]):
        self.attributes = [attr for attr in self.attributes if attr.id != str(attribute_id)]

    def reorder_attributes(self, new_order: List[Union[int, str]]):
        attr_dict = {attr.id: attr for attr in self.attributes}
        new_attributes = [attr_dict[str(attr_id)] for attr_id in new_order if str(attr_id) in attr_dict]
        self.attributes = new_attributes

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'order': self.order,
            'attributes': [attr.to_dict() for attr in self.attributes]
        }

class ViewTemplate:
    def __init__(self, name: str, description: str = "", is_default: bool = False, 
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None):
        self.name = name
        self.description = description
        self.is_default = is_default
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.sections: List[ProductSection] = []

    def add_section(self, section: ProductSection):
        self.sections.append(section)
        self.sections.sort(key=lambda s: s.order)
        self.updated_at = datetime.utcnow()

    def remove_section(self, section_id: str):
        self.sections = [section for section in self.sections if section.id != section_id]
        self.sections = [ProductSection(s.id, s.title, i, s.attributes) for i, s in enumerate(self.sections)]
        self.updated_at = datetime.utcnow()

    def reorder_sections(self, new_order: List[str]):
        section_dict = {section.id: section for section in self.sections}
        new_sections = [section_dict[section_id] for section_id in new_order if section_id in section_dict]
        self.sections = [ProductSection(s.id, s.title, i, s.attributes) for i, s in enumerate(new_sections)]
        self.updated_at = datetime.utcnow()

    def copy(self, new_id: str, new_name: str, new_description: str) -> 'ViewTemplate':
        new_view = ViewTemplate(
            id=new_id,
            name=new_name,
            description=new_description,
            is_default=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        for section in self.sections:
            new_section = ProductSection(
                id=f"{section.id}-{int(datetime.utcnow().timestamp())}",
                title=section.title,
                order=section.order,
                attributes=[
                    ProductAttribute(
                        id=f"{attr.id}-{int(datetime.utcnow().timestamp())}",
                        name=attr.name,
                        type=attr.type,
                        required=attr.required,
                        value=attr.value,
                        options=deepcopy(attr.options) if attr.type == "Picklist" else None
                    ) for attr in section.attributes
                ]
            )
            new_view.add_section(new_section)
        return new_view

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sections': [section.to_dict() for section in self.sections]
        }

class Product:
    def __init__(self, name: str, product_data: Dict[str, Any]):
        self.name = name
        self.sections: List[Dict[str, Any]] = product_data.get('structure', [])
        self.created_at = product_data.get('created_at', datetime.utcnow())
        self.updated_at = product_data.get('updated_at', datetime.utcnow())
        self.sku = next((attr['value'] for section in self.sections for attr in section['attributes'] if attr['name'] == 'SKU'), None)

    def update(self, new_data: Dict[str, Any], view_template: Optional[ViewTemplate] = None):
        if 'structure' in new_data:
            self.sections = []
            for new_section in new_data['structure']:
                section = {'title': new_section['title'], 'attributes': []}
                for new_attr in new_section['attributes']:
                    attr_id = next((a.id for s in view_template.sections for a in s.attributes if a.name == new_attr['name']), None) if view_template else None
                    if view_template and attr_id:
                        template_attr = next((a for s in view_template.sections for a in s.attributes if a.id == attr_id), None)
                        if template_attr and not template_attr.validate_value(new_attr.get('value')):
                            raise ValueError(f"Invalid value for attribute {new_attr['name']}: {new_attr.get('value')}")
                        if template_attr and template_attr.required and new_attr.get('value') is None:
                            raise ValueError(f"Attribute {new_attr['name']} is required")
                    section['attributes'].append({
                        'name': new_attr['name'],
                        'value': new_attr.get('value'),
                        'options': new_attr.get('options', [])
                    })
                self.sections.append(section)
            self.sku = next((attr['value'] for section in self.sections for attr in section['attributes'] if attr['name'] == 'SKU'), None)
            self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'structure': self.sections,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'sku': self.sku
        }

class ProductManager:
    def __init__(self):
        self.view_templates: List[ViewTemplate] = []
        self.products: List[Product] = []

    def add_view_template(self, view_template: ViewTemplate):
        self.view_templates.append(view_template)

    def get_view_template(self, view_id: str) -> Optional[ViewTemplate]:
        return next((vt for vt in self.view_templates if vt.id == view_id), None)

    def remove_view_template(self, view_id: str):
        view = self.get_view_template(view_id)
        if view and view.is_default:
            raise ValueError("Cannot delete the default view")
        self.view_templates = [vt for vt in self.view_templates if vt.id != view_id]

    def create_view_from_template(self, source_view_id: str, new_name: str, new_description: str) -> ViewTemplate:
        source_view = self.get_view_template(source_view_id)
        if not source_view:
            raise ValueError(f"Source view {source_view_id} not found")
        new_view = source_view.copy(
            new_id=f"view-{int(datetime.utcnow().timestamp())}",
            new_name=new_name,
            new_description=new_description
        )
        self.add_view_template(new_view)
        return new_view

    def add_product(self, product: Product):
        self.products.append(product)

    def get_product(self, sku: str) -> Optional[Product]:
        return next((p for p in self.products if p.sku == sku), None)

    def to_dict(self):
        return {
            'view_templates': [vt.to_dict() for vt in self.view_templates],
            'products': [p.to_dict() for p in self.products]
        }

    def load_from_dict(self, data: Dict):
        for view_data in data.get('view_templates', []):
            view = ViewTemplate(
                id=view_data['id'],
                name=view_data['name'],
                description=view_data.get('description', ''),
                is_default=view_data.get('is_default', False),
                created_at=view_data.get('created_at'),
                updated_at=view_data.get('updated_at')
            )
            for section_data in view_data.get('sections', []):
                section = ProductSection(
                    id=section_data['id'],
                    title=section_data['title'],
                    order=section_data['order']
                )
                for attr_data in section_data.get('attributes', []):
                    section.add_attribute(ProductAttribute(
                        id=attr_data['id'],
                        name=attr_data['name'],
                        type=attr_data['type'],
                        required=attr_data.get('required', False),
                        value=attr_data.get('value'),
                        options=attr_data.get('options') if attr_data['type'] == "Picklist" else None
                    ))
                view.add_section(section)
            self.add_view_template(view)

        for product_data in data.get('products', []):
            self.add_product(Product(product_data))