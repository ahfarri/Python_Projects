from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name, email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s, %(email)s, %(password)s, NOW() , NOW() );"

        return connectToMySQL('login_registration').query_db( query, data )

    @classmethod
    def get_user_email(cls, data):
        query = "SELECT * FROM users where email = %(email)s;"
        
        result = connectToMySQL('login_registration').query_db(query, data)
        
        # users = []

        # for item in result:
        #     new_item = User(item)
        #     users.append(new_item)
        return User(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("Name field requires a minimum of two characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Name field requires a minimum of two characters.")
            is_valid = False
        if len(user['email']) == 0:
            flash("Email field is a required field.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password requires a minimum of eight characters.")
            is_valid = False
        if len(User.get_user_email({"email": user['email']})) != 0:
            flash("This email is already in use.")
            is_valid = False
        if user["password"] != user["confirm_password"]:
            flash("Please ensure both password fields match.")
            is_valid = False
        return is_valid
    

