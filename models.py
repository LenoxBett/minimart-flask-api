from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Changed to False to avoid warning


class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

       # Relationships with backref
    sales = db.relationship('Sale', backref='product', lazy=True)
    purchases = db.relationship('Purchase', backref='product', lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}


class Sale(db.Model):
    __tablename__ = "Sales"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Products.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, 
                "product_id": self.product_id, 
                "product_name": self.product.name,
                "quantity": self.quantity, 
                # "created_at": self.created_at.isoformat() 
                # if self.created_at else None
                }


class Purchase(db.Model):
    __tablename__ = "Purchases"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Products.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, 
                "product_id": self.product_id,
                "product_name": self.product.name, 
                "quantity": self.quantity
                # "created_at": self.created_at.isoformat()
                # if self.created_at else None
                }


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, 
                "username": self.username, 
                "email": self.email
                }
    
# with app.app_context():
#     db.create_all()