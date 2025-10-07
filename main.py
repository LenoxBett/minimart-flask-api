from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import sentry_sdk
from models import db, Product, Sale, Purchase, User
# from flask_migrate import Migrate

sentry_sdk.init(
    dsn="https://0df18c4882363a572e85b90433bc23c6@o4509983900565504.ingest.us.sentry.io/4509984025280512",
    send_default_pii=True,
)

app = Flask(__name__)
# migrate = Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "always"
app.config["JWT_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Database setup (SQLite file: sales.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Changed to False to avoid warning

db.init_app(app)
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
@jwt_required()
def get_sales():
    all_sales = Sale.query.all()
    return jsonify([s.to_dict() for s in all_sales]), 200


@app.route('/api/sales/<int:sale_id>', methods=['GET'])
@jwt_required()
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
@jwt_required()
def get_purchases():
    all_purchases = Purchase.query.all()
    return jsonify([p.to_dict() for p in all_purchases]), 200


@app.route('/api/purchases/<int:purchase_id>', methods=['GET'])
@jwt_required()
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
@app.route("/api/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if "username" not in data or "password" not in data or "email" not in data:
        error = {"error": "Ensure username, email and password are set"}
        return jsonify(error), 400
    print(data)
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user is not None:
        error = {"error": "User with that email exists"}
        return jsonify(error), 409
    
    # Create new user
    new_user = User(
        username=data['username'], 
        email=data['email'], 
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()

    # Create JWT token
    token = create_access_token(identity=data['email'])
    return jsonify({
        'token': token,
        'user': new_user.to_dict()
    }), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    # Find user by email
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=user.email)
        return jsonify({
            "access_token": access_token,
            "user": user.to_dict()
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


if __name__ == '__main__':
    app.run(debug=True)