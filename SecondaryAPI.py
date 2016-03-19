from flask import Flask
from views.user import user

app = Flask(__name__)

API = '/db/api'


app.register_blueprint(user, url_prefix=API+'/user')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()