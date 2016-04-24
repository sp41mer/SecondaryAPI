__author__ = 'sp41mer'
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

main = Blueprint("main", __name__)
connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
cursor = connection.cursor()


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


@main.route("/clear/", methods=['POST'])
def delete_all():

    list = ['User', 'Forum', 'Thread', 'Post', 'Follow', 'Subscribe']

    for value in list:
        try:
            cursor.execute(''' delete {} from {} '''.format(value, value))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

    connection.close()
    return json.dumps({
            'code': 1,
            'response': 'OK'
    })


@main.route("/status/", methods=['GET'])
def get_status():

    list = ['user', 'forum', 'thread', 'post']
    count_dict = {}

    for el in list:
        try:
            cursor.execute(''' select count(*) from {} '''.format(el))
            count_dict[el] = cursor.fetchall()[0][0]
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })


    response = count_dict

    connection.close()

    return json.dumps({
            'code': 1,
            'response': {
                "user": response[0]['user'],
                "thread": response[0]['thread'],
                "forum": response[0]['forum'],
                "post": response[0]['post']
            }
    })


