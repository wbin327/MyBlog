# encoding=utf-8
from flask import render_template, request, jsonify
from . import auth, form
from service.ServiceInterface import ServiceInterface
service = ServiceInterface()


@auth.route('/login')
def test():
    return render_template('auth/login.html')


@auth.route('/register', methods=['post'])
def register():
    name = request.form['name']
    password = request.form['password']
    result = service.register(name, password)
    return jsonify(result)


@auth.route('/login_check', methods=['post'])
def login_check():

    username = request.form['name']
    password = request.form['password']
    result = service.login_check(username, password)
    if result['status'] is True:
        return render_template('')
    return jsonify(result)


@auth.route('/get_user', methods=['GET'])
def get():
    authorization = request.headers.get('Authorization')
    result = service.get_user(authorization)
    return jsonify(result)
