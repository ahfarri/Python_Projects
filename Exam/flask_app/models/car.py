from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re

class Car:
    def __init__( self , data ):
        self.id = data['id']
        self.price = data['price']
        self.description = data['description']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.created_on = data['created_on']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def add_car(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, users_id, created_on, updated_at ) VALUES ( %(price)s , %(model)s, %(make)s, %(year)s, %(description)s, %(users_id)s, NOW() , NOW() );"

        return connectToMySQL('cars_schema').query_db( query, data )

    @classmethod
    def get_cars(cls):
        query = "SELECT * FROM cars left join users on cars.users_id = users.id;"

        results = connectToMySQL('cars_schema').query_db(query)

        cars = []

        for item in results:
            car = cls(item)
            new_item = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_on': item['users.created_on'],
                'updated_at': item['users.updated_at']
            }
            car.user = new_item
            cars.append(car)
        return cars

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"

        connectToMySQL('cars_schema').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"

        results = connectToMySQL('cars_schema').query_db(query, data)

        return Car(results[0])
    
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM cars left join users on cars.users_id = users.id WHERE cars.id = %(id)s;"

        results = connectToMySQL('cars_schema').query_db(query, data)

        cars = []

        for item in results:
            car = cls(item)
            new_item = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_on': item['users.created_on'],
                'updated_at': item['users.updated_at']
            }
            car.user = new_item
            cars.append(car)
        return cars

    @classmethod
    def edit_one(cls, data):
        query = "UPDATE cars SET price=%(price)s, description =%(description)s, model =%(model)s, make =%(make)s, year =%(year)s, users_id =%(users_id)s WHERE id=%(id)s;"

        connectToMySQL('cars_schema').query_db(query, data)

    @staticmethod
    def validate_car(car):
        is_valid = True
        if len(car['year']) <= 0:
            flash("Year field must be greater than 0.")
            is_valid = False
        if len(car['price']) <= 0:
            flash("Price field must be greater than 0.")
            is_valid = False
        if len(car['model']) <= 0:
            flash("Model field is a required field.")
            is_valid = False
        if len(car['make']) <= 0:
            flash("Make field is a required field.")
            is_valid = False
        if len(car['description']) <= 0:
            flash("Description field is a required field.")
            is_valid = False
        return is_valid