from mongoengine import Document, StringField, FloatField, ListField

class CoreProductSchema(Document):
    meta={'collection':'core_products'}
    product_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    tags=ListField(StringField())
    category = StringField()
    rating=FloatField(min_value=0,max_value=5)



