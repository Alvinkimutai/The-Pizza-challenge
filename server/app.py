#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource, reqparse
import os
restaurant_pizzas_args = reqparse.RequestParser()


restaurant_pizzas_args.add_argument('price', type= int, required =True, help ='price is required and must be between 1 and 30')
restaurant_pizzas_args.add_argument('pizza_id', type=int, required =True, help='pizza_id is required and must be an integer')
restaurant_pizzas_args.add_argument('restaurant_id', type=int, required= True, help='restaurant_id is required and must be an integer')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>The Pizza challenge</h1>'

class Restaurants(Resource):
    def get(self):
        restaurants = []
        for restaurant in Restaurant.query.all():
            restaurant_dict ={"address": restaurant.address,
                               "id": restaurant.id,
                               "name":restaurant.name
                               }
            restaurants.append(restaurant_dict)
        return make_response(jsonify(restaurants), 200)
    
class RestaurantsId(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            return make_response(jsonify(restaurant_dict), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)
        
    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response(jsonify(restaurant.to_dict()), 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}))
        
class Pizzas(Resource):
    def get(self):
        all_pizzas = []
        pizzas = Pizza.query.all()
        for pizza in pizzas:
            pizzas_dict = pizza.to_dict()
            all_pizzas.append(pizzas_dict)
        return make_response(jsonify(all_pizzas), 200)
    
class RestaurantPizzas(Resource):
    def post(self):
        data = restaurant_pizzas_args.parse_args()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")
        if 1<=price<=30:
            new_restaurant_pizza = RestaurantPizza(price= price, pizza_id=pizza_id, restaurant_id= restaurant_id)
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return make_response(jsonify(new_restaurant_pizza.to_dict()), 201)
        else:
            return make_response(jsonify({"errors":["validation errors"]}), 400)
        
    
api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantsId, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)
