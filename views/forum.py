__author__ = 'sp41mer'
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

    forum = request.args.get("forum", type=str, default=None)
    related = request.args.getlist('related', type=str)

    if forum:

        try:
            cursor.execute(
                '''select * from Forum f where f.short_name='{}' '''.format(forum))
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


@forum.route("/listPosts/", methods=['GET'])
def listPosts():

    forum = request.args.get("forum", type=str, default=None)
    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')
    related = request.args.getlist('related', type=str)

    if limit:
        trueLimit = 'LIMIT '+limit
    else:
        trueLimit = ''

    if order != 'asc' and order != 'desc':
        return json.dumps({
                'code': 3,
                'response': 'Error'
            })

    if since:
        trueSince = ' and date >='+since
    else:
        trueSince = ''
    if forum:
        try:
            cursor.execute(
                '''select * from Post p where p.forum='{}' {} order by p.date {} {} '''.format(forum, trueSince, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)
        responseArrayToJson = []

        for eachPost in response:
            if eachPost['isApproved'] == 0:
                eachPost['isApproved'] = 'false'
            else:
                eachPost['isApproved'] = 'true'

            if eachPost['isDeleted'] == 0:
                eachPost['isDeleted'] = 'false'
            else:
                eachPost['isDeleted'] = 'true'

            if eachPost['isEdited'] == 0:
                eachPost['isEdited'] = 'false'
            else:
                eachPost['isEdited'] = 'true'

            if eachPost['isHighlighted'] == 0:
                eachPost['isHighlighted'] = 'false'
            else:
                eachPost['isHighlighted'] = 'true'

            if eachPost['isSpam'] == 0:
                eachPost['isSpam'] = 'false'
            else:
                eachPost['isSpam'] = 'true'

            eachPost['date'] = str(eachPost['date'])

            if 'user' in related and cursor.execute(''' select * from User u where u.email='{}' '''.format(eachPost['user'])):
                responseInFor = dictfetchall(cursor)
                cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(eachPost['user']))
                followers = cursor.fetchall()
                true_followers = []
                for sublist in followers:
                    for val in sublist:
                        true_followers.append(val)

                cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(eachPost['user']))
                followees = cursor.fetchall()
                true_followees = []
                for sublist in followees:
                    for val in sublist:
                        true_followees.append(val)

                cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(eachPost['user']))
                threads = cursor.fetchall()
                true_threads = []
                for sublist in threads:
                    for val in sublist:
                        true_threads.append(val)

                eachPost['user'] = {
                    'about': responseInFor[0]['about'],
                    'email': responseInFor[0]['email'],
                    'followers': true_followers,
                    'followees': true_followees,
                    'subscriptions': true_threads,
                    'id': responseInFor[0]['id'],
                    'isAnonymous':responseInFor[0]['isAnonymous'],
                    'name': responseInFor[0]['name'],
                    'username': responseInFor[0]['username']
                }

            if 'forum' in related and cursor.execute('''select * from Forum f where f.short_name='{}' '''.format(eachPost['forum'])):
                responseInFor = dictfetchall(cursor)
                eachPost['forum'] = responseInFor[0]

            if 'thread' in related and cursor.execute('''select * from Thread t where t.id={} '''.format(eachPost['thread'])):
                responseInFor = dictfetchall(cursor)
                if responseInFor[0]['isDeleted'] == 0:
                    responseInFor[0]['isDeleted'] = 'false'
                else:
                    responseInFor[0]['isDeleted'] = 'true'

                if responseInFor[0]['isClosed'] == 0:
                    responseInFor[0]['isClosed'] = 'false'
                else:
                    responseInFor[0]['isClosed'] = 'true'

                responseInFor[0]['date'] = str(responseInFor[0]['date'])


                eachPost['thread'] = responseInFor[0]

            responseArrayToJson.append({
                "date": eachPost['date'],
                "dislikes": eachPost['dislikes'],
                "forum": eachPost['forum'],
                "id": eachPost['id'],
                "isApproved": eachPost['isApproved'],
                "isDeleted": eachPost['isDeleted'],
                "isEdited": eachPost['isEdited'],
                "isHighlighted": eachPost['isHighlighted'],
                "isSpam": eachPost['isSpam'],
                "likes": eachPost['likes'],
                "message": eachPost['message'],
                "parent": eachPost['parent'],
                "points": eachPost['points'],
                "thread": eachPost['thread'],
                "user": eachPost['user']
            })

        connection.close()

        return json.dumps({
                'code': 0,
                'response': responseArrayToJson
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@forum.route("/listUsers/", methods=['GET'])
def list_users():

    Forum = request.args.get("forum", type=str, default=None)

    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')

    if limit:
        trueLimit = 'LIMIT '+limit
    else:
        trueLimit = ''

    if order != 'asc' and order != 'desc':
        return json.dumps({
                'code': 3,
                'response': 'Error'
            })

    if since:
        trueSince = ' and date >='+since
    else:
        trueSince = ''

    if Forum:

        try:
            cursor.execute(
                '''select * from User u where {} u.email in ( select distinct p.user from Post p where p.forum='{}' ) order by u.name {} {} '''.format(trueSince, Forum, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)
        mainUsers = []
        for eachUser in response:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(eachUser['email']))

            responseInFor = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(eachUser['email']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(eachUser['email']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(eachUser['email']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

            if responseInFor[0]['isAnonymous'] == 0:
                responseInFor[0]['isAnonymous'] = 'false'
            else:
                responseInFor[0]['isAnonymous'] = 'true'

            mainUsers.append({
                'about': responseInFor[0]['about'],
                'email': responseInFor[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': responseInFor[0]['id'],
                'isAnonymous': responseInFor[0]['isAnonymous'],
                'name': responseInFor[0]['name'],
                'username': responseInFor[0]['username']
            })

        connection.close()

        return json.dumps({
            'code': 0,
            'response': mainUsers
        })

    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@forum.route("/listThreads/", methods=['GET'])
def list_threads():

    forum = request.args.get("forum", type=str, default=None)
    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')
    related = request.args.getlist('related', type=str)

    if limit:
        trueLimit = 'LIMIT '+limit
    else:
        trueLimit = ''

    if order != 'asc' and order != 'desc':
        return json.dumps({
                'code': 3,
                'response': 'Error'
            })

    if since:
        trueSince = ' and date >='+since
    else:
        trueSince = ''

    if forum:

        try:
            cursor.execute(
                '''select * from Thread t where t.forum='{}' {} order by t.date {} {} '''.format(forum, trueSince, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)
        for eachThread in response:
            if eachThread['isDeleted'] == 0:
                eachThread['isDeleted'] = 'false'
            else:
                eachThread['isDeleted'] = 'true'

            if eachThread['isClosed'] == 0:
                eachThread['isClosed'] = 'false'
            else:
                eachThread['isClosed'] = 'true'

            eachThread['date'] = str(eachThread['date'])

        connection.close()

        return json.dumps({
            'code': 0,
            'response': response
        })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })



