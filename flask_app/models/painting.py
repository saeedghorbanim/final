from flask import flash

from flask_app.models.users import User
from flask_app.config.mysqlconnection import connectToMySQL

class Painting():

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None


    @classmethod
    def create_painting(cls, data):
        
        query = 'INSERT INTO paintings (title, description, price, users_id) VALUES (%(title)s, %(description)s, %(price)s, %(users_id)s);'
        result = connectToMySQL('exam').query_db(query, data)

        return result


    
    @classmethod
    def get_all_paintings(cls):
        query = 'SELECT * FROM paintings JOIN users ON paintings.users_id = users.id;'

        results = connectToMySQL('exam').query_db(query)

        paintings = []

        for item in results:
            painting = cls(item)
            user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at']
                }
            painting.user = User(user_data)
            paintings.append(painting)

        return paintings




    @classmethod
    def get_painting_by_id(cls,data):
        query = 'SELECT * FROM paintings JOIN users ON paintings.users_id = users.id WHERE paintings.id = %(id)s;'

        result = connectToMySQL('exam').query_db(query, data)

        painting = cls(result[0])
        user_data = {
            'id' : result[0]['users.id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        painting.user = User(user_data)

        return painting
        


    @classmethod
    def update_painting(cls, data):
        query = 'UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;'

        connectToMySQL('exam').query_db(query, data)


    @classmethod
    def delete_painting(cls, data):

        query = 'DELETE FROM paintings WHERE id = %(id)s;'

        connectToMySQL('exam').query_db(query, data)



    @staticmethod 
    def validate_painting(data):

        is_valid = True

        if len(data['title']) < 1:
            flash("Title of painting not valid.")
            is_valid = False


        if len(data['description']) < 10 or len(data['description']) > 600:
            flash("description should be more than 2 or less than 600 characters.")
            is_valid = False


        if data['price'] == '':
            flash("please insert a price")
            is_valid = False

        return is_valid