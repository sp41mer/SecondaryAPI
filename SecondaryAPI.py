import json
from flask import Flask, request
from flask_restful import reqparse
from flask.ext.mysql import MySQL
from flask_restful import Resource, Api

mysql = MySQL()
app = Flask(__name__)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
class CreateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO tblUser (UserName,Password) VALUES ('{}', '{}')'''.format(_userEmail,_userPassword))
            #cursor.callproc('spCreateUser',(_userEmail,_userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'StatusCode':'200','Message': 'User creation success'}
            else:
                return {'StatusCode':'1000','Message': str(data[0])}
        except Exception as e:
            return {'error': str(e)}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=int, location='args')
        args = parser.parse_args()
        return {'Message': args}




api.add_resource(CreateUser, '/CreateUser')


if __name__ == '__main__':
    app.run(debug=True)