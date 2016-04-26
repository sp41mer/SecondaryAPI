__author__ = 'sp41mer'
# listPosts
# listThreads
# listUsers
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

forum = Blueprint("forum", __name__)
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


@forum.route("/create/", methods=['POST'])
def create():

    try:
        requestData = json.loads(request.data)
    except:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })

    if requestData['name'] and requestData['short_name'] and requestData['user']:

        try:
            cursor.execute(
                '''insert into `Forum` (`name`, `short_name`, `user`) values ('{}','{}','{}') '''.format(
                    requestData['name'].encode("utf8"), requestData['short_name'], requestData['user']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        try:
            cursor.execute(
                '''select * from Forum f where f.short_name='{}' '''.format(requestData['short_name']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        connection.close()

        return json.dumps({
            "code": 0,
            "response": {
                "id": response[0]['id'],
                "name": response[0]['name'],
                "short_name": response[0]['short_name'],
                "user": response[0]['user']
            }
        })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@forum.route("/details/", methods=['GET'])
def details():

    forum_name = request.args.get("forum", type=str, default=None)
    related = request.args.getlist('related', type=str)

    if forum_name:

        try:
            cursor.execute(
                '''select * from Forum f where f.short_name='{}' '''.format(forum_name))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })


        if cursor.rowcount == 0:
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        try:
         cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(response[0]['user']))
         if cursor.rowcount == 0:
                return json.dumps({'code':5, 'response': 'User not found'})

         userDict = dictfetchall(cursor)

         cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(response[0]['user']))
         followers = cursor.fetchall()
         true_followers = []
         for sublist in followers:
            for val in sublist:
                true_followers.append(val)

         cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(response[0]['user']))
         followees = cursor.fetchall()
         true_followees = []
         for sublist in followees:
            for val in sublist:
                true_followees.append(val)

         cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(response[0]['user']))
         threads = cursor.fetchall()
         true_threads = []
         for sublist in threads:
            for val in sublist:
                true_threads.append(val)


        except (MySQLdb.Error, MySQLdb.Warning) as e:
                connection.close()
                return e
        connection.close()

        return json.dumps({
            "code": 0,
            "response": {
                "id": response[0]['id'],
                "name": response[0]['name'],
                "short_name": response[0]['short_name'],
                "user": {
                    'about': userDict[0]['about'],
                    'email': userDict[0]['email'],
                    'followers': true_followers,
                    'followees': true_followees,
                    'subscriptions': true_threads,
                    'id': userDict[0]['id'],
                    'isAnonymous': userDict[0]['isAnonymous'],
                    'name': userDict[0]['name'],
                    'username': userDict[0]['username']
                     }
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })

