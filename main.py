from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "always"
app.config["JWT_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Database setup (SQLite file: sales.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# In-memory users list for demo purposes
users = []

# ________MODELS_______
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }


# Create tables
with app.app_context():
    db.create_all()


# ---------------- Products Routes ----------------
@app.route('/api/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({"error": "name and price are required"}), 400

    product = Product(name=name, price=float(price))
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added successfully", "product": product.to_dict()}), 201


@app.route('/api/products', methods=['GET'])
@jwt_required()
def get_products():
    all_products = Product.query.all()
    return jsonify([p.to_dict() for p in all_products]), 200


@app.route('/api/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if "name" in data:
        product.name = data["name"]
    if "price" in data:
        product.price = float(data["price"])

    db.session.commit()
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product with ID {product_id} deleted successfully"}), 200


# ---------------- SALES ROUTES -----------
@app.route('/api/sales', methods=['POST'])
@jwt_required()
def add_sale():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if product_id is None or quantity is None:
        return jsonify({"error": "product_id and quantity are required"}), 400

    sale = Sale(product_id=int(product_id), quantity=float(quantity))
    db.session.add(sale)
    db.session.commit()

    return jsonify({"message": "Sale recorded successfully", "sale": sale.to_dict()}), 201


@app.route('/api/sales', methods=['GET'])
def get_sales():
    all_sales = Sale.query.all()
    return jsonify([s.to_dict() for s in all_sales]), 200


@app.route('/api/sales/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Sale not found"}), 404
    return jsonify(sale.to_dict()), 200


@app.route('/api/sales/<int:sale_id>', methods=['PUT'])
@jwt_required()
def update_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    data = request.get_json()
    if "product_id" in data:
        sale.product_id = int(data["product_id"])
    if "quantity" in data:
        sale.quantity = float(data["quantity"])

    db.session.commit()
    return jsonify({"message": "Sale updated successfully", "sale": sale.to_dict()}), 200


@app.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@jwt_required()
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"error": "Sale not found"}), 404

    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": f"Sale with ID {sale_id} deleted successfully"}), 200


# ---------------- Purchases Routes ----------------
@app.route('/api/purchases', methods=['POST'])
@jwt_required()
def add_purchase():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if product_id is None or quantity is None:
        return jsonify({"error": "product_id and quantity are required"}), 400

    purchase = Purchase(product_id=int(product_id), quantity=float(quantity))
    db.session.add(purchase)
    db.session.commit()

    return jsonify({"message": "Purchase recorded successfully", "purchase": purchase.to_dict()}), 201


@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    all_purchases = Purchase.query.all()
    return jsonify([p.to_dict() for p in all_purchases]), 200


@app.route('/api/purchases/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404
    return jsonify(purchase.to_dict()), 200


@app.route('/api/purchases/<int:purchase_id>', methods=['PUT'])
@jwt_required()
def update_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404

    data = request.get_json()
    if "product_id" in data:
        purchase.product_id = int(data["product_id"])
    if "quantity" in data:
        purchase.quantity = float(data["quantity"])

    db.session.commit()
    return jsonify({"message": "Purchase updated successfully", "purchase": purchase.to_dict()}), 200


@app.route('/api/purchases/<int:purchase_id>', methods=['DELETE'])
@jwt_required()
def delete_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    if not purchase:
        return jsonify({"error": "Purchase not found"}), 404

    db.session.delete(purchase)
    db.session.commit()
    return jsonify({"message": f"Purchase with ID {purchase_id} deleted successfully"}), 200


# ---------------- Auth ----------------
@app.route("/api/users")
def get_users():
    return jsonify(users), 200


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if "username" not in data or "password" not in data:
        error = {"error": "Ensure username and password are set"}
        return jsonify(error), 400
    else:
        users.append(data)
        return jsonify(data), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Simple login
    if username == "admin" and password == "password123":
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(debug=True)
