from flask_app.config.mysqlconnection import connectToMySQL

class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        # Create an empty list to append our instances of friends
        dojos = []
        # Iterate over the db results and create instances of friends with cls.
        for item in results:
            dojos.append(cls(item))
        return dojos

    @classmethod
    def create(cls, data):
        query = "INSERT INTO dojos ( name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"

        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )

    @classmethod
    def get_all_ninjas(cls, data):
        query = "SELECT * FROM dojos left join ninjas on dojos.id =ninjas.dojo_id where dojo_id = %(id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)
        # Create an empty list to append our instances of friends
        # ninjas = []
        # # # Iterate over the db results and create instances of friends with cls.
        # for item in results:
        #     ninjas.append(Ninja(item))
        return results
    
    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s;"

    #     results = connectToMySQL('users_schema').query_db(query, data)

    #     user = User(results[0])

    #     return user
    
    # @classmethod
    # def edit_one(cls, data):
    #     query = "UPDATE users SET first_name=%(first_name)s, last_name =%(last_name)s, email=%(email)s WHERE id=%(id)s;"

    #     connectToMySQL('users_schema').query_db(query, data)




    # @classmethod
    # def delete_one(cls, data):
    #     query = "DELETE FROM users WHERE id = %(id)s;"

    #     connectToMySQL('users_schema').query_db(query, data)

    
