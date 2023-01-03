from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import cx_Oracle

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'your-secret-key'

# Replace username, password, and host with your own values
connection = cx_Oracle.connect('username', 'password', 'host:port/sid')

class UserResource(Resource):
    def get(self):
        # Retrieve data from the database
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return {'users': users}
    
    def post(self):
        # Insert data into the database
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO users (name, age) VALUES (:name, :age)',
            {'name': 'John', 'age': 30}
        )
        connection.commit()
        return {'message': 'User added'}, 201
    
    def put(self):
        # Update data in the database
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE users SET age = :age WHERE name = :name',
            {'name': 'John', 'age': 35}
        )
        connection.commit()
        return {'message': 'User updated'}, 200
    
    def delete(self):
        # Delete data from the database
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE name = :name', {'name': 'John'})
        connection.commit()
        return {'message': 'User deleted'}, 200

api.add_resource(UserResource, '/users')

@app.route('/login')
def login():
    # Implement login and return a JWT
    return {'access_token': 'your-jwt'}

@app.route('/protected')
@jwt_required
def protected():
    # Protected endpoint
    return {'message': 'You are authorized to see this message'}

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
'''
To use the API, you will need to send a POST request to the /login endpoint with the correct credentials to obtain a JWT. Then, you can use the JWT to access the protected endpoints by including it in the Authorization header of your request:

Authorization: Bearer your-jwt
'''
    
