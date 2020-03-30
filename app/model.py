from app import db


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship("Category", back_populates="products")

    def __init__(self, name, fk):
        self.name = name
        self.category_id = fk

    @property
    def serialized(self):
        return {'id': self.id, 'product': self.name, 'category': {'id': self.category.id, 'category': self.category.name}}


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    products = db.relationship('Product', backref=db.backref('products', lazy=True))

    def __init__(self, name):
        self.name = name

    @property
    def serialized(self):
        products = [i.name for i in self.products] if len(self.products) > 0 else "none"
        return {'id': self.id, 'category': self.name, 'products': products}
