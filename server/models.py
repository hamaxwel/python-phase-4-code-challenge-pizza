from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "restaurant_pizzas": [
                restaurant_pizza.to_dict() for restaurant_pizza in self.pizzas
            ]
        }


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    _price = db.Column('price', db.Float, nullable=False)

    # Property for price with validation
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30")
        self._price = value

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "restaurant_id": self.restaurant_id,
            "pizza_id": self.pizza_id,
            "restaurant": self.restaurant.to_dict(),  # Include restaurant details
            "pizza": self.pizza.to_dict(),  # Include pizza details
        }
