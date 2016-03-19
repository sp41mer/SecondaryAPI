__author__ = 'sp41mer'
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb

user = Blueprint("user", __name__)

connection = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="ItemListDb")
cursor = connection.cursor()


@user.route("/create", methods=['POST'])
def create():
    req_params = {'user':'pinus@hui', 'password': 'huina'}
    try:
     cursor.execute('''insert into `tblUser` (`UserName`, `Password`)
                  values ('{}','{}').format(req_params['user'],req_params['password']) ''')
     result = cursor.fetchall()
    except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return 'pinus'
    return str(result)