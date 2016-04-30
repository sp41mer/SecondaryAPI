__author__ = 'sp41mer'
# list
# listPosts ENEMY!!!!!1!!!!11!!
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

thread = Blueprint("thread", __name__)


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


@thread.route("/close/", methods=['POST'])
def close():

    requestData = json.loads(request.data)

    if requestData['thread']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

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
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

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
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

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
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()
        try:
            cursor.execute(''' delete from Subscribe where thread={} and user='{}' '''.format(requestData['thread'], requestData['user']))
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


@thread.route("/create/", methods=['POST'])
def create():

    requestData = json.loads(request.data)

    if requestData['forum'] and requestData['title'] and str(requestData['isClosed']) and requestData['user'] and requestData['date'] and requestData[
        'message'] and requestData['slug']:

        if requestData.get('isClosed', 0):
            requestData['isClosed'] = 1

        if requestData.get('isDeleted', 0):
            requestData['isDeleted'] = 1

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(
            '''insert into `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`, `isDeleted`, `isClosed`) values ('{}', '{}','{}','{}','{}','{}','{}','{}') '''.format(
                requestData['forum'], requestData['title'].encode("utf8"), requestData['user'], requestData['date'], requestData['message'].encode("utf8"), requestData['slug'].encode("utf8"), requestData.get('isDeleted', 0),
                requestData.get('isClosed', 0)))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        try:
            cursor.execute(''' select * from Thread t where t.date='{}' '''.format(requestData['date']))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = False
        else:
            response[0]['isDeleted'] = True

        if response[0]['isClosed'] == 0:
            response[0]['isClosed'] = False
        else:
            response[0]['isClosed'] = True

        response[0]['date'] = str(response[0]['date'])

        connection.close()

        return json.dumps({
                'code': 0,
                'response': {
                    "date": response[0]['date'],
                    "forum": response[0]['forum'],
                    "id": response[0]['id'],
                    "isClosed": response[0]['isClosed'],
                    "isDeleted": response[0]['isDeleted'],
                    "message": response[0]['message'],
                    "slug": response[0]['slug'],
                    "title": response[0]['title'],
                    "user": response[0]['user']
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/remove/", methods=['POST'])
def remove():
    requestData = json.loads(request.data)

    if requestData['thread']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select count(*) from post where thread={} and isDeleted != 0 '''.format(requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        number = cursor.fetchall()[0][0]

        try:
            cursor.execute(''' update Post set isDeleted=1 where thread={} '''.format(requestData['thread']))
            cursor.execute(''' update Thread set isDeleted=1, posts={} where id={} '''.format(number, requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        connection.close()

        response = {
            'thread': requestData['thread']
        }

        return json.dumps({
                'code': 0,
                'response': response
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/restore/", methods=['POST'])
def restore():

    requestData = json.loads(request.data)

    if requestData['thread']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select count(*) from post where thread={} and isDeleted != 0 '''.format(requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        number = cursor.fetchall()[0][0]

        try:
            cursor.execute(''' update Post set isDeleted=0 where thread={} '''.format(requestData['thread']))
            cursor.execute(''' update Thread set isDeleted=0, posts={} where id={} '''.format(number, requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 4,
                'response': 'Error'
            })

        connection.close()

        response = {
            'thread': requestData['thread']
        }

        return json.dumps({
                'code': 0,
                'response': response
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/vote/", methods=['POST'])
def vote():

    requestData = json.loads(request.data)

    if requestData['thread'] and requestData['vote']:

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()
        try:
            if requestData['vote'] == -1:
                cursor.execute(''' update Thread t set dislikes=dislikes+1, points=points-1 where t.id={} '''.format(requestData['thread']))
            elif requestData['vote'] == 1:
                cursor.execute(''' update Thread t set likes=likes+1, points=points+1 where t.id={} '''.format(requestData['thread']))
            else:
                return json.dumps({
                'code': 3,
                'response': 'Error'
            })

            connection.commit()

            cursor.execute(''' select * from Thread t where t.id={} '''.format(requestData['thread']))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = False
        else:
            response[0]['isDeleted'] = True

        if response[0]['isClosed'] == 0:
            response[0]['isClosed'] = False
        else:
            response[0]['isClosed'] = True

        response[0]['date'] = str(response[0]['date'])

        return json.dumps({
                'code': 0,
                'response': {
                    "date": response[0]['date'],
                    "forum": response[0]['forum'],
                    "id": response[0]['id'],
                    "isClosed": response[0]['isClosed'],
                    "isDeleted": response[0]['isDeleted'],
                    "message": response[0]['message'],
                    "slug": response[0]['slug'],
                    "title": response[0]['title'],
                    "user": response[0]['user']
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/update/", methods=['POST'])
def update():
    requestData = json.loads(request.data)

    if requestData['message'] and requestData['slug'] and requestData['thread']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' update Thread t set t.message='{}', t.slug='{}' where t.id={} '''.format(requestData['message'], requestData['slug'], requestData['thread']))
            cursor.execute(''' select * from Thread t where t.id={} '''.format(requestData['thread']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = False
        else:
            response[0]['isDeleted'] = True

        if response[0]['isClosed'] == 0:
            response[0]['isClosed'] = False
        else:
            response[0]['isClosed'] = True

        response[0]['date'] = str(response[0]['date'])

        return json.dumps({
                'code': 0,
                'response': {
                    "date": response[0]['date'],
                    "forum": response[0]['forum'],
                    "id": response[0]['id'],
                    "isClosed": response[0]['isClosed'],
                    "isDeleted": response[0]['isDeleted'],
                    "message": response[0]['message'],
                    "slug": response[0]['slug'],
                    "title": response[0]['title'],
                    "user": response[0]['user']
                }
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/details/", methods=['GET'])
def details():

    thread_id = request.args.get("thread", type=int, default=None)
    related = request.args.getlist('related', type=str)

    if len([item for item in related if item not in ['user', 'forum']]) > 0:
        return json.dumps({
                'code': 3,
                'response': 'Error'
            })

    if thread_id:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Thread t where t.id='{}' '''.format(thread_id))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)


        if 'user' in related and cursor.execute(''' select * from User u where u.email='{}' '''.format(response[0]['user'])):
            responseInFor = dictfetchall(cursor)
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

            response[0]['user'] = {
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

        if 'forum' in related and cursor.execute('''select * from Forum f where f.short_name='{}' '''.format(response[0]['forum'])):
            responseInFor = dictfetchall(cursor)
            response[0]['forum'] = responseInFor[0]

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = False
        else:
            response[0]['isDeleted'] = True

        if response[0]['isClosed'] == 0:
            response[0]['isClosed'] = False
        else:
            response[0]['isClosed'] = True

        response[0]['date'] = str(response[0]['date'])

        connection.close()

        return json.dumps({
                'code': 0,
                'response': {
                    "date": response[0]['date'],
                    "forum": response[0]['forum'],
                    "id": response[0]['id'],
                    "isClosed": response[0]['isClosed'],
                    "isDeleted": response[0]['isDeleted'],
                    "message": response[0]['message'],
                    "slug": response[0]['slug'],
                    "title": response[0]['title'],
                    "user": response[0]['user']
                }
            })

    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })


@thread.route("/list/", methods=['GET'])
def list_threads():

    user_email = request.args.get("user", default=None)
    forum_name = request.args.get("forum", default=None)

    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')

    if order not in ['asc', 'desc']:
        return json.dumps({
                'code': 3,
                'response': 'Error'
            })

    if limit:
        trueLimit = 'LIMIT '+limit
    else:
        trueLimit = ''

    if since:
        trueSince = ' and date >='+since
    else:
        trueSince = ''

    if user_email:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Thread t where t.user='{}' {} order by t.date {} {} '''.format(user_email, trueSince, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)
        connection.close()
        responseArrayToJson = []

        for eachThread in response:
            if eachThread['isDeleted'] == 0:
                eachThread['isDeleted'] = False
            else:
                eachThread['isDeleted'] = True

            if eachThread['isClosed'] == 0:
                eachThread['isClosed'] = False
            else:
                eachThread['isClosed'] = True

            eachThread['date'] = str(eachThread['date'])

            responseArrayToJson.append({"date": eachThread['date'],
                                        "forum": eachThread['forum'],
                                        "id": eachThread['id'],
                                        "isClosed": eachThread['isClosed'],
                                        "isDeleted": eachThread['isDeleted'],
                                        "message": eachThread['message'],
                                        "slug": eachThread['slug'],
                                        "title": eachThread['title'],
                                        "user": eachThread['user']})

        return json.dumps({
                'code': 0,
                'response': responseArrayToJson
            })

    elif forum_name:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Thread t where t.forum='{}' {} order by t.date {} {} '''.format(forum_name, trueSince, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        connection.close()

        responseArrayToJson = []

        for eachThread in response:
            if eachThread['isDeleted'] == 0:
                eachThread['isDeleted'] = False
            else:
                eachThread['isDeleted'] = True

            if eachThread['isClosed'] == 0:
                eachThread['isClosed'] = False
            else:
                eachThread['isClosed'] = True

            eachThread['date'] = str(eachThread['date'])

            responseArrayToJson.append({"date": eachThread['date'],
                                        "forum": eachThread['forum'],
                                        "id": eachThread['id'],
                                        "isClosed": eachThread['isClosed'],
                                        "isDeleted": eachThread['isDeleted'],
                                        "message": eachThread['message'],
                                        "slug": eachThread['slug'],
                                        "title": eachThread['title'],
                                        "user": eachThread['user']})

        return json.dumps({
                'code': 0,
                'response': responseArrayToJson
            })

    elif forum_name and user_email:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Thread t where t.user='{}' and t.forum='{}' {} order by t.date {} {} '''.format(user_email, forum_name, trueSince, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        response = dictfetchall(cursor)

        connection.close()

        responseArrayToJson = []

        for eachThread in response:
            if eachThread['isDeleted'] == 0:
                eachThread['isDeleted'] = False
            else:
                eachThread['isDeleted'] = True

            if eachThread['isClosed'] == 0:
                eachThread['isClosed'] = False
            else:
                eachThread['isClosed'] = True

            eachThread['date'] = str(eachThread['date'])

            responseArrayToJson.append({"date": eachThread['date'],
                                        "forum": eachThread['forum'],
                                        "id": eachThread['id'],
                                        "isClosed": eachThread['isClosed'],
                                        "isDeleted": eachThread['isDeleted'],
                                        "message": eachThread['message'],
                                        "slug": eachThread['slug'],
                                        "title": eachThread['title'],
                                        "user": eachThread['user']})

        return json.dumps({
                'code': 0,
                'response': responseArrayToJson
            })
    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })