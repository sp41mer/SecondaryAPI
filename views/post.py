__author__ = 'sp41mer'
from flask import Blueprint, request
from flask.ext.mysql import MySQL
import MySQLdb
import json
import itertools

post = Blueprint("post", __name__)
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

@post.route("/restore/", methods=['POST'])
def restore():
    requestData = json.loads(request.data)

    if requestData['post']:
        try:
            cursor.execute(''' update Post p set p.isDeleted=0 where p.id={} '''.format(requestData['post']))
            cursor.execute(''' select thread from Post where id={} '''.format(requestData['post']))
            targetId = cursor.fetchall()[0][0]
            cursor.execute(''' update Thread set posts=posts+1 where id={} '''.format(targetId))
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
                'post': requestData['post']
                }
            })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
        })

@post.route("/create/", methods=['POST'])
def create():
    requestData = json.loads(request.data)

    if requestData['date'] and requestData['thread'] and requestData['message'] and requestData['user'] and requestData['forum']:

        #needs some refactoring( uebischno kakto:( )

        if not requestData.get('isApproved', 0):
            requestData['isApproved'] = 1

        if requestData.get('isHighlighted', 0):
            requestData['isHighlighted'] = 1

        if requestData.get('isEdited', 0):
            requestData['isEdited'] = 1

        if requestData.get('isEdited', 0):
            requestData['isSpam'] = 1

        if requestData.get('isDeleted', 0):
            requestData['isDeleted'] = 1



        try:
            if requestData.get('parent', None):
                 cursor.execute(
                    ''' insert into `Post` (`thread`, `user`, `forum`, `date`, `message`, `dislikes`, `likes`, `points`, `parent`, `isHighlighted`, `isApproved`, `isEdited`, `isSpam`, `isDeleted`) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') '''.format(
                        requestData['thread'], requestData['user'], requestData['forum'], requestData['date'], requestData['message'], 0, 0, 0,
                        requestData['parent'], requestData.get('isHighlighted', 0), requestData.get('isApproved', 0), requestData.get('isEdited', 0),
                        requestData.get('isSpam', 0),  requestData.get('isDeleted', 0)))

            else:
                cursor.execute(''' insert into `Post` (`thread`, `user`, `forum`, `date`, `message`, `dislikes`, `likes`, `points`, `parent`, `isHighlighted`, `isApproved`, `isEdited`, `isSpam`, `isDeleted`) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', NULL, '{}', '{}', '{}', '{}', '{}') '''.format(
                        requestData['thread'], requestData['user'], requestData['forum'], requestData['date'], requestData['message'], 0, 0, 0,
                        requestData.get('isHighlighted', 0), requestData.get('isApproved', 0), requestData.get('isEdited', 0),
                        requestData.get('isSpam', 0),  requestData.get('isDeleted', 0)))

        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 4,
            'response': 'Error'
            })

        try:
            cursor.execute(''' select * from Post p where p.date='{}' '''.format(requestData['date']))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Not Found'
            })

        response = dictfetchall(cursor)

        if response[0]['isApproved'] == 0:
            response[0]['isApproved'] = 'false'
        else:
            response[0]['isApproved'] = 'true'

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = 'false'
        else:
            response[0]['isDeleted'] = 'true'

        if response[0]['isEdited'] == 0:
            response[0]['isEdited'] = 'false'
        else:
            response[0]['isEdited'] = 'true'

        if response[0]['isHighlighted'] == 0:
            response[0]['isHighlighted'] = 'false'
        else:
            response[0]['isHighlighted'] = 'true'

        if response[0]['isSpam'] == 0:
            response[0]['isSpam'] = 'false'
        else:
            response[0]['isSpam'] = 'true'

        connection.close()

        return json.dumps({
            'code': 0,
            'response': {
                "date": response[0]['date'],
                "forum": response[0]['forum'],
                "id": response[0]['id'],
                "isApproved": response[0]['isApproved'],
                "isDeleted": response[0]['isDeleted'],
                "isEdited": response[0]['isEdited'],
                "isHighlighted": response[0]['isHighlighted'],
                "isSpam": response[0]['isSpam'],
                "message": response[0]['message'],
                "parent": response[0]['parent'],
                "thread": response[0]['thread'],
                "user": response[0]['user']
            }
        })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
            })


@post.route("/remove/", methods=['POST'])
def remove():

    requestData = json.loads(request.data)

    if requestData['post']:

        try:
            cursor.execute(''' update Post p set p.isDeleted=1 where p.id={} '''.format(requestData['post']))
            cursor.execute(''' select thread from Post where id={} '''.format(requestData['post']))
            id_thread = cursor.fetchall()[0][0]
            cursor.execute(''' update Thread set posts=posts-1 where id={} '''.format(id_thread))
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
                'post': requestData['post']
                }
            })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
            })


@post.route("/update/", methods=['POST'])
def update():
    requestData = json.loads(request.data)

    if requestData['post'] and requestData['message']:

        c, conn = connection()
        try:
            c.execute(''' update Post p set p.message='{}' where p.id={} '''.format(requestData['message'], requestData['post']))
            c.execute(''' select * from Post p where p.id={} '''.format(requestData['post']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return json.dumps({
            'code': 4,
            'response': 'Error'
            })

        response = dictfetchall(cursor)

        if response[0]['isApproved'] == 0:
            response[0]['isApproved'] = 'false'
        else:
            response[0]['isApproved'] = 'true'

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = 'false'
        else:
            response[0]['isDeleted'] = 'true'

        if response[0]['isEdited'] == 0:
            response[0]['isEdited'] = 'false'
        else:
            response[0]['isEdited'] = 'true'

        if response[0]['isHighlighted'] == 0:
            response[0]['isHighlighted'] = 'false'
        else:
            response[0]['isHighlighted'] = 'true'

        if response[0]['isSpam'] == 0:
            response[0]['isSpam'] = 'false'
        else:
            response[0]['isSpam'] = 'true'

        connection.close()

        return json.dumps({
            'code': 0,
            'response': {
                "date": response[0]['date'],
                "forum": response[0]['forum'],
                "id": response[0]['id'],
                "isApproved": response[0]['isApproved'],
                "isDeleted": response[0]['isDeleted'],
                "isEdited": response[0]['isEdited'],
                "isHighlighted": response[0]['isHighlighted'],
                "isSpam": response[0]['isSpam'],
                "message": response[0]['message'],
                "parent": response[0]['parent'],
                "thread": response[0]['thread'],
                "user": response[0]['user']
            }
        })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
            })


@post.route("/vote/", methods=['POST'])
def vote():
    requestData = json.loads(request.data)

    if requestData['post'] and requestData['vote']:

        if requestData['vote'] != 1 and requestData['vote'] != -1:
            return json.dumps({
            'code': 3,
            'response': 'Error'
            })

        try:
            if requestData['vote'] == -1:
                cursor.execute(''' update Post p set dislikes=dislikes+1, points=points-1 where p.id={} '''.format(requestData['post']))
            else:
                cursor.execute(''' update Post p set likes=likes+1, points=points+1 where p.id={} '''.format(requestData['post']))
            connection.commit()

            cursor.execute(''' select * from Post p where p.id={} '''.format(requestData['post']))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Error'
            })

        response = dictfetchall(cursor)

        if response[0]['isApproved'] == 0:
            response[0]['isApproved'] = 'false'
        else:
            response[0]['isApproved'] = 'true'

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = 'false'
        else:
            response[0]['isDeleted'] = 'true'

        if response[0]['isEdited'] == 0:
            response[0]['isEdited'] = 'false'
        else:
            response[0]['isEdited'] = 'true'

        if response[0]['isHighlighted'] == 0:
            response[0]['isHighlighted'] = 'false'
        else:
            response[0]['isHighlighted'] = 'true'

        if response[0]['isSpam'] == 0:
            response[0]['isSpam'] = 'false'
        else:
            response[0]['isSpam'] = 'true'

        connection.close()

        return json.dumps({
            'code': 0,
            'response': {
                "date": response[0]['date'],
                "forum": response[0]['forum'],
                "id": response[0]['id'],
                "isApproved": response[0]['isApproved'],
                "isDeleted": response[0]['isDeleted'],
                "isEdited": response[0]['isEdited'],
                "isHighlighted": response[0]['isHighlighted'],
                "isSpam": response[0]['isSpam'],
                "message": response[0]['message'],
                "parent": response[0]['parent'],
                "thread": response[0]['thread'],
                "user": response[0]['user']
            }
        })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
            })


@post.route("/details/", methods=['GET'])
def details():

    post = request.args.get('post', type=int, default=None)
    related = request.args.getlist('related', type=str)

    if post:
        try:
            cursor.execute(''' select * from Post p where p.id='{}' '''.format(post))
        except (MySQLdb.Error, MySQLdb.Warning):
            connection.close()
            return json.dumps({
            'code': 1,
            'response': 'Invalid request'
            })

        if cursor.rowcount == 0:
            return json.dumps({
            'code': 1,
            'response': 'Invalid request'
            })

        response = dictfetchall(cursor)

        if response[0]['isApproved'] == 0:
            response[0]['isApproved'] = 'false'
        else:
            response[0]['isApproved'] = 'true'

        if response[0]['isDeleted'] == 0:
            response[0]['isDeleted'] = 'false'
        else:
            response[0]['isDeleted'] = 'true'

        if response[0]['isEdited'] == 0:
            response[0]['isEdited'] = 'false'
        else:
            response[0]['isEdited'] = 'true'

        if response[0]['isHighlighted'] == 0:
            response[0]['isHighlighted'] = 'false'
        else:
            response[0]['isHighlighted'] = 'true'

        if response[0]['isSpam'] == 0:
            response[0]['isSpam'] = 'false'
        else:
            response[0]['isSpam'] = 'true'

        connection.close()

        return json.dumps({
            'code': 0,
            'response': {
                "date": response[0]['date'],
                "forum": response[0]['forum'],
                "id": response[0]['id'],
                "isApproved": response[0]['isApproved'],
                "isDeleted": response[0]['isDeleted'],
                "isEdited": response[0]['isEdited'],
                "isHighlighted": response[0]['isHighlighted'],
                "isSpam": response[0]['isSpam'],
                "message": response[0]['message'],
                "parent": response[0]['parent'],
                "thread": response[0]['thread'],
                "user": response[0]['user']
            }
        })
    else:
        return json.dumps({
            'code': 2,
            'response': 'Invalid request'
            })