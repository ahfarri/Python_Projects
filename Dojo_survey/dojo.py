from mysqlconnection import connectToMySQL
from flask import flash
# model the class after the friend table from our database
class Dojo:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # class method to save our friend to the database
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO dojos ( first_name , location , language, comment, created_at, updated_at ) VALUES ( %(name)s , %(location)s , %(language)s , %(comment)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('dojo_survey_schema').query_db( query, data )


    @staticmethod
    def validate_dojo(dojo):
        is_valid = True # we assume this is true
        if len(dojo['name']) == 0:
            flash("Name field is a required field.")
            is_valid = False
        if len(dojo['location']) == 0:
            flash("Location field is a required field.")
            is_valid = False
        if len(dojo['language']) == 0:
            flash("Language field is a required field.")
            is_valid = False
        if len(dojo['comment']) == 0:
            flash("Comment field is a required field.")
            is_valid = False
        return is_valid