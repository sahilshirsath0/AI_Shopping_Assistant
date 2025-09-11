import os
from flask import Flask, request, jsonify
from mongoengine import connect, Document, StringField, FloatField, ReferenceField, ListField

# Define the directory for local image uploads
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MongoDB connection
MONGO_URI = "mongodb+srv://sahil:SahilOracle2245@cluster0.vivxrsr.mongodb.net/"
connect(host=MONGO_URI, alias='default')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Schemas
class CoreProductSchema(Document):
    meta = {'collection': 'core_products'}
    product_id = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    tags = ListField(StringField())
    category = StringField()
    rating = FloatField(min_value=0, max_value=5)
    image = StringField()


class ProductRefSchema(Document):
    meta = {'collection': 'product_refs'}
    product = ReferenceField(CoreProductSchema, required=True, unique=True)
    theme = StringField(required=True)
    stock_quantity = FloatField(min_value=0)


# ---------------- Single Upload ----------------
@app.route('/upload_product', methods=['POST'])
def upload_product():
    try:
        data = request.form

        # Core product
        core_product_data = {
            'product_id': data.get('product_id'),
            'name': data.get('name'),
            'description': data.get('description'),
            'price': float(data.get('price')),
            'tags': [tag.strip() for tag in data.get('tags', '').split(',') if tag.strip()],
            'category': data.get('category'),
            'rating': float(data.get('rating'))
        }
        new_core_product = CoreProductSchema(**core_product_data).save()

        # Reference product
        ref_product_data = {
            'product': new_core_product,
            'theme': data.get('theme'),
            'stock_quantity': float(data.get('stock_quantity'))
        }
        new_ref_product = ProductRefSchema(**ref_product_data).save()

        return jsonify({
            "message": "Product created successfully",
            "core_product_id": str(new_core_product.id),
            "ref_product_id": str(new_ref_product.id)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Bulk Upload ----------------
@app.route('/upload_products_bulk', methods=['POST'])
def upload_products_bulk():
    try:
        products = request.get_json()  # Expecting a JSON array
        created = []

        for prod in products:
            core_product_data = {
                'product_id': prod.get('product_id'),
                'name': prod.get('name'),
                'description': prod.get('description'),
                'price': float(prod.get('price')),
                'tags': [tag.strip() for tag in prod.get('tags', [])],
                'category': prod.get('category'),
                'rating': float(prod.get('rating')),
                 'image': prod.get('image')

            }
            new_core_product = CoreProductSchema(**core_product_data).save()

            ref_product_data = {
                'product': new_core_product,
                'theme': prod.get('theme'),
                'stock_quantity': float(prod.get('stock_quantity'))
            }
            new_ref_product = ProductRefSchema(**ref_product_data).save()

            created.append({
                "core_product_id": str(new_core_product.id),
                "ref_product_id": str(new_ref_product.id)
            })

        return jsonify({
            "message": f"{len(created)} products created successfully",
            "products": created
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
