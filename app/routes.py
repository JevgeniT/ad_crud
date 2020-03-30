from flask import request, jsonify
from app import db, app
from app.model import Category, Product
from sqlalchemy import exc


@app.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({'response': [i.serialized for i in products]})


@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    if not product_exists_id(id):
        return jsonify({'error': 'there is no such product'})

    product = Product.query.get(id)
    return jsonify({'response': product.serialized})


@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['product']
    product_category = request.json['category']

    if product_exists_name(name):
        return jsonify({'error': 'this product already exists in database'})
    elif not category_exists_id(product_category):
        return jsonify({'error': 'there is no such category'})
    else:
        product = Product(name, product_category)
        db.session.add(product)
        db.session.commit()
        return jsonify({'response': {'added': product.serialized}})


@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    name = request.json['product']

    if not product_exists_id(id):
        return jsonify({'error': 'cannot update non-existent product'})
    elif product_exists_name(name):
        return jsonify({'error': 'this product already exists in database'})
    else:
        product = Product.query.get(id)
        product.name = name
        db.session.commit()
        return jsonify({'response': {'updated': product.serialized}})


@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    if not product_exists_id(id):
        return jsonify({'error': 'cannot delete non-existent product'})

    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'response': 'deleted'})


@app.route('/category', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({'response': [i.serialized for i in categories]})


@app.route('/category/<id>', methods=['GET'])
def get_category(id):
    if not category_exists_id(id):
        return jsonify({'error': 'there is no such category'})
    category = Category.query.get(id)
    return jsonify({'response': category.serialized})


@app.route('/category', methods=['POST'])
def add_category():
    name = request.json['category']

    if category_exists_name(name):
        return jsonify({'error': 'this category already exists in database'})
    else:
        category = Category(name)
        db.session.add(Category(name))
        db.session.commit()
        return jsonify({'response': category.serialized})


@app.route('/category/<id>', methods=['DELETE'])
def delete_category(id):
    if not category_exists_id(id):
        return jsonify({'error': 'cannot delete non-existent category'})

    try:
        category = Category.query.get(id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'response': 'deleted'})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'cannot delete category that has products'})


@app.route('/category/<id>', methods=['PUT'])
def update_category(id):
    name = request.json['category']
    if not category_exists_id(id):
        return jsonify({'error': 'cannot update non-existent category'})
    elif category_exists_name(name):
        return jsonify({'error': 'this category name is being used'})

    category = Category.query.get(id)
    category.name = name
    db.session.commit()
    return jsonify({'response': {'updated': category.serialized}})


def product_exists_id(id):
    return db.session.query(db.exists().where(Product.id == id)).scalar()


def product_exists_name(name):
    return db.session.query(db.exists().where(Product.name == name)).scalar()


def category_exists_id(id):
    return db.session.query(db.exists().where(Category.id == id)).scalar()


def category_exists_name(name):
    return db.session.query(db.exists().where(Category.name == name)).scalar()
