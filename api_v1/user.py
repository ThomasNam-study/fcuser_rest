from flask import jsonify, request

from model import Fcuser, db
from . import api


@api.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'error': 'No argument'}), 400

        if password != re_password:
            return jsonify({'error': 'Wrong password'}), 400

        fcuser = Fcuser()

        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return jsonify(), 201

    users = Fcuser.query.all()

    return jsonify([user.serialize for user in users])


@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)
    elif request.method == 'DELETE':
        Fcuser.query.delete(Fcuser.id == uid)
        return jsonify()

    data = request.get_json()

    userid = data.get('userid')
    username = data.get('username')
    password = data.get('password')

    updated_data = {}

    if userid:
        updated_data['userid'] = userid

    if username:
        updated_data['username'] = username

    if password:
        updated_data['password'] = password

    Fcuser.query.filter(Fcuser.id == uid).update(updated_data)

    user = Fcuser.query.filter(Fcuser.id == uid).first()
    return jsonify(user.serialize)