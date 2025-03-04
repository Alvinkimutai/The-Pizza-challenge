from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # I added one to many relationship between restaurant_pizzas and 
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates= "restaurant", cascade='all, delete-orphan')

    # I added serialization rules to remove this attribute from the Json output
    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    #I added one to many relationship between pizza and restaurant_pizzas
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates="pizza", cascade='all, delete-orphan')

    #I added serialization rules to only include details of pizza only
    serialize_rules = ('-restaurant_pizzas',)


    def __repr__(self):
        return f'<Pizza {self.name}, {self.ingredients}>'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('Restaurant', back_populates="restaurant_pizzas")

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    pizza = db.relationship('Pizza', back_populates="restaurant_pizzas")
    # add serialization rules
    serialize_rules = ('-restaurant.restaurant_pizzas','-pizza.restaurant_pizzas',)

    # add validation to ensure the price is of appropriate range
    @validates('price')
    def validate_price(self, key, value):
        if 1<=value<=30:
            return value
        else:
            raise ValueError('Invalid Price')

    def __repr__(self):
        return f'<RestaurantPizza ${self.price}>'
