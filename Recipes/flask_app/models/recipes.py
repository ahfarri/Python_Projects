from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.minutes = data['minutes']
        self.instructions = data['instructions']
        self.made = data['made_on']
        self.created_on = data['created_on']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes ( name , description, minutes, instructions, made_on, users_id, created_on, updated_at ) VALUES ( %(name)s , %(description)s, %(minutes)s, %(instructions)s, %(made_on)s, %(users_id)s, NOW() , NOW() );"

        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_recipes(cls):
        query = "SELECT * FROM recipes;"
        
        result = connectToMySQL('recipes_schema').query_db(query)
        
        recipes = []

        for item in result:
            recipes.append(cls(item))
        return recipes

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"

        results = connectToMySQL('recipes_schema').query_db(query, data)

        user = Recipe(results[0])

        return user

    @classmethod
    def edit_one(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description =%(description)s, instructions =%(instructions)s, minutes =%(minutes)s, made_on =%(made_on)s WHERE id=%(id)s;"

        connectToMySQL('recipes_schema').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name field requires a minimum of three characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description field requires a minimum of three characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions field requires a minimum of three characters.")
            is_valid = False
        if len(recipe['made_on']) != 10:
            flash("Date made is a required field.")
            is_valid = False
        if len(recipe['minutes']) < 2:
            flash("Under 30 minutes is a required field.")
            is_valid = False
        return is_valid