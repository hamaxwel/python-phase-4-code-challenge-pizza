from flask import Flask, jsonify, request
from models import Restaurant, Pizza, RestaurantPizza, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict(include_pizzas=True))


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    price = data.get('price')

    # Validate input
    if not pizza_id or not restaurant_id:
        return jsonify({"errors": ["pizza_id and restaurant_id are required"]}), 400
    if not db.session.get(Pizza, pizza_id) or not db.session.get(Restaurant, restaurant_id):
        return jsonify({"errors": ["Invalid pizza_id or restaurant_id"]}), 404
    if price is None or price < 1 or price > 30:
        return jsonify({"errors": ["price must be between 1 and 30"]}), 400

    # Create new RestaurantPizza
    try:
        new_restaurant_pizza = RestaurantPizza(
            pizza_id=pizza_id, restaurant_id=restaurant_id, price=price
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Return RestaurantPizza with related Pizza data
        response_data = new_restaurant_pizza.to_dict()
        return jsonify(response_data), 201
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400


@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"errors": [str(e)]}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5555)
