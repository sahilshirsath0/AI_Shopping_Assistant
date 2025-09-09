from mongoengine import Document, StringField, FloatField,ReferenceField
from .CoreProductSchema import CoreProductSchema

class ProductRefSchema(Document):
    meta={'collection':'product_refs'}
    product = ReferenceField(CoreProductSchema, required=True, unique=True)
    theme=StringField(required=True)
    stock_quantity = FloatField(min_value=0)
