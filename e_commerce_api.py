from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from password import password
from marshmallow import fields
from marshmallow import ValidationError
from created_tables import Customer, CustomerAccount, Order, Product, db, app

ma = Marshmallow(app)


class CustomerSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

class Meta:
    fields = ('name', 'email', 'phone', 'id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class CustomerAccountSchema(ma.Schema):
    id = fields.Int(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    customer_id = fields.Int(required=True)

class Meta:
    fields = ('id', 'username', 'password', 'customer_id')

customeraccount_schema = CustomerAccountSchema()
customeraccounts_schema = CustomerAccountSchema(many=True)


class OrderSchema(ma.Schema):
    id = fields.Int(required=True)
    date = fields.String(required=True)
    customer_id = fields.Int(required=True)

class Meta:
    fields = ('id', 'date', 'customer_id')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class ProductSchema(ma.Schema):
    id = fields.Int(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)

class Meta:
    fields = ('id', 'name', 'price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# ------------------------------------------------

@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id) 
    return customer_schema.jsonify(customer)


@app.route('/customer', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer) 
    db.session.commit()
    return jsonify({"message": "New customer added successfully"}), 201

@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id) 
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()
    return jsonify({"message": "Customer details updated successfully"}), 200

@app.route('/customer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer removed successfully"}), 200

# -----------------------------------------------
@app.route('/customeraccount', methods=['GET'])
def get_customer_account():
    customer_account = CustomerAccount.query.all() 
    return customeraccounts_schema.jsonify(customer_account)


@app.route('/customeraccount', methods=['POST'])
def add_customer_account():
    try:
        customer_data = customeraccount_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer_account = CustomerAccount(id=customer_data['id'], username=customer_data['username'], password=customer_data['password'], customer_id=customer_data['customer_id'])
    db.session.add(new_customer_account) 
    db.session.commit()
    return jsonify({"message": "New customer account added successfully"}), 201


@app.route('/customeraccount/<int:id>', methods=['PUT'])
def update_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id) 
    try:
        customer_data = customeraccount_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_account.username = customer_data['username']
    customer_account.email = customer_data['password']
    customer_account.phone = customer_data['customer_id']
    db.session.commit()
    return jsonify({"message": "Customer account details updated successfully"}), 200


@app.route('/customeraccount/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    customer_account = CustomerAccount.query.get_or_404(id)
    db.session.delete(customer_account)
    db.session.commit()
    return jsonify({"message": "Customer account removed successfully"}), 200

# -----------------------------------------------
@app.route('/product/<int:id>', methods=['GET'])
def get_product_info(id):
    product = Product.query.get_or_404(id) 
    return product_schema.jsonify(product)


@app.route('/product', methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_product = Product(id=product_data['id'], name=product_data['name'], price=product_data['price'])
    db.session.add(new_product) 
    db.session.commit()
    return jsonify({"message": "New product added successfully"}), 201


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id) 
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product.id = product_data['id']
    product.name = product_data['name']
    product.price = product_data['price']
    db.session.commit()
    return jsonify({"message": "Product details updated successfully"}), 200

@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product removed successfully"}), 200

@app.route('/product', methods=['GET'])
def product_list():
    product = Product.query.all() 
    return products_schema.jsonify(product)

# -----------------------------------------------

@app.route('/orders', methods=['POST'])
def place_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_order = Order(id=order_data['id'], date=order_data['date'], customer_id=order_data['customer_id'])
    db.session.add(new_order) 
    db.session.commit()
    return jsonify({"message": "New order added successfully"}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id) 
    return order_schema.jsonify(order)



@app.route('/trackorders/<int:id>', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id) 
    return order_schema.jsonify(order)




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)