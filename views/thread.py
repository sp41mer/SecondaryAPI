__author__ = 'sp41mer'
# create
# details
# list
# listPosts
# remove
# restore
# update
# vote
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

thread = Blueprint("thread", __name__)
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


@thread.route("/close/", methods=['POST'])
def close():

    requestData = json.loads(request.data)

    if requestData['thread']:

        try:
            cursor.execute(''' update Thread t set isClosed=1 where t.id={} '''.format(requestData['thread']))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        connection.close()

        return json.dumps({
                'code': 1,
                'response': {
                    'thread': requestData['thread']
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })

@thread.route("/open/", methods=['POST'])
def open():

    requestData = json.loads(request.data)

    if requestData['thread']:

        try:
            cursor.execute(''' update Thread t set isClosed=0 where t.id={} '''.format(requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        connection.close()

        return json.dumps({
                'code': 1,
                'response': {
                    'thread': requestData['thread']
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/subscribe/", methods=['POST'])
def subscribe():

    requestData = json.loads(request.data)

    if requestData['thread'] and requestData['user']:

        try:
            cursor.execute(''' insert into `Subscribe` (`thread`, `user`) values ('{}', '{}') '''.format(requestData['thread'], requestData['user']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        connection.close()

        return json.dumps({
                'code': 1,
                'response': {
                    'thread': requestData['thread'],
                    'user': requestData['user']
                }
        })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/unsubscribe/", methods=['POST'])
def unsubscribe():

    requestData = json.loads(request.data)

    if requestData['thread'] and requestData['user']:

        c, conn = connection()
        try:
            c.execute(''' delete from Subscribe where thread={} and user='{}' '''.format(requestData['thread'], requestData['user']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        conn.close()

        return json.dumps({
                'code': 1,
                'response': {
                    'thread': requestData['thread'],
                    'user': requestData['user']
                }
         })

    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })



