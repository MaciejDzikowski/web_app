#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort, session, redirect, make_response, \
    flash, render_template, url_for
from functools import wraps
import json

app = Flask(__name__)

app.secret_key = 'your secret'
app.config['SESSION_TYPE'] = 'filesystem'


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return decorated


@app.route('/')
def hello1st():
    return 'Hello, World!'


@app.route('/hello')
def hello():
    return 'Hello, Boi!'


@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_info():
    return f'{request.method}'


@app.route('/show_data', methods=['POST'])
def show():
    if not request.json:
        abort(400)
    print(request.json)
    return json.dumps(request.json)  # jsonify(request.json)


@app.route('/pretty_print_name', methods=['GET', 'POST'])
def pretty():
    if not request.json:
        abort(400)
    sname = request.json['name']
    ssurename = request.json['surename']
    name = str(sname)
    surename = str(ssurename)
    s = 'Na imię mu %s, a nazwisko jego %s' % (name, surename)
    return s


@app.route('/counter')
def counter():
    x = session.get('x', None)
    if not x:
        session['x'] = 1
    else:
        session['x'] += 1
    return str(session['x'])


@app.route('/train', methods=['GET'])
def train_req():
    return 'observation'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.authorization and request.authorization.username == 'TRAIN' \
            and request.authorization.password == 'TuN3L':
        session['logged_in'] = True
        flash('Zostales zalogowany!')
        return redirect('/hello')
    else:
        return make_response('Nie mozna zweryfikowac!', 401,
                             {
                                 'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/logout', methods=['GET', 'POST'])
@auth_required
def logout():
    session.pop('logged_in', None)
    flash('Zostales wylogowany!')
    return redirect('/')


@app.route('/trains')
@auth_required
def trains():
    return '<h1>TRRRRRain</h1>'


if __name__ == '__main__':
    app.run(debug=True)