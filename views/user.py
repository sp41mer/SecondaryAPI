__author__ = 'sp41mer'
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

user = Blueprint("user", __name__)


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


@user.route("/create/", methods=['POST'])
def create():
    request_data = json.loads(request.data)

    if request_data['isAnonymous'] == True:
        request_data['isAnonymous'] = 1
        anon = True
    else:
        request_data['isAnonymous'] = 0
        anon = False

    if (request_data.get('username',None) and request_data.get('about',None) and request_data.get('name',None) and request_data.get('email', None)) or anon:

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute('''insert into `User` (`username`, `email`, `about`, `name`, `isAnonymous`)
                    values ('{}','{}','{}','{}','{}') '''.format(request_data['username'],
                                                                 request_data['email'], request_data['about'],
                                                                 request_data['name'], request_data['isAnonymous']))
            result_create = cursor.fetchall()
            connection.commit()

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            connection.close()
            return json.dumps({
            'code': 4,
            'response': 'SQL fail'
        })

        try:
            cursor.execute('''select * from User where email ='{}' '''.format(request_data['email']))
            selected_id = cursor._rows[0][0]
            connection.close()

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            connection.close()
            return json.dumps({
            'code': 4,
            'response': 'SQL fail'
        })


        return json.dumps({
        'code': 0,
        'response': {
            "about": request_data['about'],
            "email": request_data['email'],
            "id": selected_id,
            "isAnonymous": anon,
            "name": request_data['name'],
            "username": request_data['username']
        }
        })
    else:
        return json.dumps({
            'code': 3,
            'response': 'Invalid request'
        })


@user.route("/details/", methods=['GET'])
def details():
    get_pars = request.args.get("user", type=str, default=None)
    if get_pars:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
         cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(get_pars))
         if cursor.rowcount == 0:
                return json.dumps({'code':5, 'response': 'User not found'})

         response = dictfetchall(cursor)

         cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(get_pars))
         followers = cursor.fetchall()
         true_followers = []
         for sublist in followers:
            for val in sublist:
                true_followers.append(val)

         cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(get_pars))
         followees = cursor.fetchall()
         true_followees = []
         for sublist in followees:
            for val in sublist:
                true_followees.append(val)

         cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(get_pars))
         threads = cursor.fetchall()
         true_threads = []
         for sublist in threads:
            for val in sublist:
                true_threads.append(val)


        except (MySQLdb.Error, MySQLdb.Warning) as e:
                connection.close()
                return e
        if response[0]['isAnonymous'] == 0:
            response[0]['isAnonymous'] = False
        else:
            response[0]['isAnonymous'] = True

        return json.dumps({
            'code': 0,
            'response': {
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous':response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            }
        })
    else:
        return json.dumps({
            'code': 3,
            'response': 'Invalid request'
        })

@user.route("/follow/", methods=['POST'])
def follow():

    request_data = json.loads(request.data)

    if request_data['follower'] and request_data['followee']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute('''insert into `Follow` (`follower`, `followee`) values ('{}','{}') '''.format(request_data['follower'],
                                                                                                 request_data['followee']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not Found'
            })

        try:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(request_data['follower']))
            if cursor.rowcount == 0:
                return json.dumps({'code': 5, 'response': 'Not found'})

            response = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(request_data['follower']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(request_data['follower']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(request_data['follower']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not Found'
            })

        if response[0]['isAnonymous'] == 0:
            response[0]['isAnonymous'] = False
        else:
            response[0]['isAnonymous'] = True

        return json.dumps({
            'code': 1,
            'response': {
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous':response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            }
        })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })

@user.route("/updateProfile/", methods=['POST'])
def updateProfile():

    request_data = json.loads(request.data)

    if request_data['about'] and request_data['user'] and request_data['name']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' update User u set name='{}', about='{}' where u.email='{}' '''.format(request_data['name'], request_data['about'], request_data['user']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not found'
        })

        try:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(request_data['user']))
            if cursor.rowcount == 0:
                return json.dumps({'code': 5, 'response': 'Not found'})

            response = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(request_data['user']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(request_data['user']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(request_data['user']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not Found'
            })

        if response[0]['isAnonymous'] == 0:
            response[0]['isAnonymous'] = False
        else:
            response[0]['isAnonymous'] = True

        return json.dumps({
            'code': 1,
            'response': {
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous':response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            }
        })
    else:
        json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })

@user.route("/unfollow/", methods=['POST'])
def unfollow():

    request_data = json.loads(request.data)

    if request_data['follower'] and request_data['followee']:
        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' delete from Follow where follower='{}' and followee='{}' '''.format(request_data['follower'], request_data['followee']))
            connection.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 4,
            'response': 'Unknown error'
            })

        try:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(request_data['follower']))
            if cursor.rowcount == 0:
                return json.dumps({'code': 5, 'response': 'Not found'})

            response = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(request_data['follower']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(request_data['follower']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(request_data['follower']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not Found'
            })

        if response[0]['isAnonymous'] == 0:
            response[0]['isAnonymous'] = False
        else:
            response[0]['isAnonymous'] = True

        return json.dumps({
            'code': 1,
            'response': {
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous': response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            }
        })

    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })


@user.route("/listFollowers/", methods=['GET'])
def listFollowers():

    requestData = request.args.get("user", type=str, default=None)

    if requestData:

        limit = request.args.get("limit", type=int, default=None)

        order = request.args.get("order", type=str, default='desc')

        if limit:
            trueLimit = 'LIMIT '+limit
        else:
            trueLimit = ''

        if order != 'asc' and order != 'desc':
            return json.dumps({
                'code': 3,
                'response': 'Error'
            })

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            trueSinceId = 'and u.id >='+since_id
        else:
            trueSinceId = ''

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Follow f join User u on f.follower = u.email where f.followee='{}' and u.id {} order by u.name {} {} '''.format(requestData, trueSinceId, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        mainResponse = dictfetchall(cursor)
        mainFollowers = []
        for eachUser in mainResponse:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(eachUser['follower']))

            response = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(eachUser['follower']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(eachUser['follower']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(eachUser['follower']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

            if response[0]['isAnonymous'] == 0:
                response[0]['isAnonymous'] = False
            else:
                response[0]['isAnonymous'] = True

            mainFollowers.append({
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous': response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            })

        connection.close()

        return json.dumps({
            'code': 0,
            'response': mainFollowers
        })
    else:
        json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })


@user.route("/listFollowing/", methods=['GET'])
def list_following():
    requestData = request.args.get("user", type=str, default=None)

    if requestData:

        limit = request.args.get("limit", type=int, default=None)

        order = request.args.get("order", type=str, default='desc')

        if limit:
            trueLimit = 'LIMIT '+limit
        else:
            trueLimit = ''

        if order != 'asc' and order != 'desc':
            return json.dumps({
                'code': 3,
                'response': 'Error'
            })

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            trueSinceId = 'and u.id >='+since_id
        else:
            trueSinceId = ''

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Follow f join User u on f.followee = u.email where f.follower='{}' and u.id {} order by u.name {} {} '''.format(requestData, trueSinceId, order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })

        mainResponse = dictfetchall(cursor)
        mainFollowers = []
        for eachUser in mainResponse:
            cursor.execute('''SELECT * FROM User WHERE email = '{}' '''.format(eachUser['followee']))

            response = dictfetchall(cursor)

            cursor.execute('''SELECT follower FROM Follow WHERE followee = '{}' '''.format(eachUser['followee']))
            followers = cursor.fetchall()
            true_followers = []
            for sublist in followers:
                for val in sublist:
                    true_followers.append(val)

            cursor.execute('''SELECT followee FROM Follow WHERE follower = '{}' '''.format(eachUser['followee']))
            followees = cursor.fetchall()
            true_followees = []
            for sublist in followees:
                for val in sublist:
                    true_followees.append(val)

            cursor.execute('''SELECT thread FROM Subscribe WHERE user = '{}' '''.format(eachUser['followee']))
            threads = cursor.fetchall()
            true_threads = []
            for sublist in threads:
                for val in sublist:
                    true_threads.append(val)

            if response[0]['isAnonymous'] == 0:
                response[0]['isAnonymous'] =False
            else:
                response[0]['isAnonymous'] = True

            mainFollowers.append({
                'about': response[0]['about'],
                'email': response[0]['email'],
                'followers': true_followers,
                'followees': true_followees,
                'subscriptions': true_threads,
                'id': response[0]['id'],
                'isAnonymous': response[0]['isAnonymous'],
                'name': response[0]['name'],
                'username': response[0]['username']
            })

        connection.close()

        return json.dumps({
            'code': 0,
            'response': mainFollowers
        })
    else:
        json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })

@user.route("/listPosts/", methods=['GET'])
def list_posts_users():

    requestData = request.args.get("user", type=str, default=None)

    if requestData:

        limit = request.args.get("limit", type=int, default=None)

        order = request.args.get("order", type=str, default='desc')

        if limit:
            trueLimit = 'LIMIT '+limit
        else:
            trueLimit = ''

        if order != 'asc' and order != 'desc':
            return json.dumps({
                'code': 3,
                'response': 'Error'
            })

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            trueSinceId = ' and u.id >='+since_id
        else:
            trueSinceId = ''

        connection = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="root",
                             db="forum_db")
        cursor = connection.cursor()

        try:
            cursor.execute(''' select * from Post p where p.user = '{}' {} order by p.date {} {} '''.format(requestData, trueSinceId , order, trueLimit))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
                'code': 1,
                'response': 'Error'
            })
        response = dictfetchall(cursor)
        responseArrayToJson = []
        connection.close()
        for eachPost in response:
            if eachPost['isApproved'] == 0:
                eachPost['isApproved'] = False
            else:
                eachPost['isApproved'] = True

            if eachPost['isDeleted'] == 0:
                eachPost['isDeleted'] = False
            else:
                eachPost['isDeleted'] = True

            if eachPost['isEdited'] == 0:
                eachPost['isEdited'] = False
            else:
                eachPost['isEdited'] = True

            if eachPost['isHighlighted'] == 0:
                eachPost['isHighlighted'] = False
            else:
                eachPost['isHighlighted'] = True

            if eachPost['isSpam'] == 0:
                eachPost['isSpam'] = False
            else:
                eachPost['isSpam'] = True
            eachPost['date'] = str(eachPost['date'])

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

        return json.dumps({
                'code': 0,
                'response': responseArrayToJson
            })

    else:
        return json.dumps({
                'code': 2,
                'response': 'Error'
            })




