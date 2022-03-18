import random
import uuid
from flask import Flask, url_for, redirect, render_template, session, flash, request
import mysql.connector
from db_connect import *

app = Flask(__name__, template_folder='templates')
app.secret_key = "marcel"


@app.route('/account')
def account():
    return render_template('account.jinja2')


@app.route('/account-login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_login = request.form['username_l']
        password_login = request.form['password_l']
        check_username_and_password_exist_login = 'SELECT * FROM users WHERE username = %s AND password = %s'
        value_check_username_and_password_exist_login = (username_login, password_login)
        cursor.execute(check_username_and_password_exist_login, value_check_username_and_password_exist_login)
        if cursor.fetchone():
            session['user'] = username_login
            return redirect(url_for('chats'))
        else:
            flash('user isn\'t exist try other password or username')
    return render_template('login.jinja2')


@app.route('/account-register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username_register = request.form['username_r']
        password_register = request.form['password_r']
        check_username_exist_register = 'SELECT COUNT(*) FROM users WHERE username = %s'
        value_username_exist_register = (username_register,)
        cursor.execute(check_username_exist_register, value_username_exist_register)
        if len(username_register) == 0 or len(password_register) == 0:
            flash(
                'your password or username is null, your password must have 8 to 128 characters and username must have 4 to 128 characters')
        else:
            if cursor.fetchone()[1]:
                flash('username already exist, try other', 'info')
            else:
                username_add_to_db = 'INSERT INTO users (username, password) VALUES(%s, %s)'
                value_username_add_to_db = (username_register, password_register)
                cursor.execute(username_add_to_db, value_username_add_to_db)
                db_connect.commit()
                return redirect(url_for('login'))

    return render_template('register.jinja2')


@app.route('/add-room', methods=['POST', 'GET'])
def add_chat():
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            name_room = request.form['room_name']
            password_room = request.form['room_password']
            id_room_result = uuid.uuid1()
            id_room_result = ''.join(str(id_room_result))
            add_chat_info_to_db = 'INSERT INTO chats (chat_name, id_chat, password_chat, user) VALUES (%s, %s, %s, %s)'
            values_add_chat_info_to_db = (name_room, id_room_result, password_room, user)
            cursor.execute(add_chat_info_to_db, values_add_chat_info_to_db)
            db_connect.commit()
            return redirect(url_for('chats'))
        return render_template('add_chat.jinja2')
    else:
        return redirect(url_for('login'))


@app.route('/')
@app.route('/rooms')
def chats():
    if 'user' in session:
        user = session['user']
        select_all_chats_user = 'SELECT chat_name FROM chats WHERE user = %s'
        value_select_all_chats_user = (user, )
        cursor.execute(select_all_chats_user, value_select_all_chats_user)
        select_all_chats_user_result = cursor.fetchall()
        return render_template('chats.jinja2', chat=select_all_chats_user_result)
    else:
        return redirect(url_for('login'))


@app.route('/join-room', methods=['POST', 'GET'])
def join_room():
    if 'user' in session:
        if request.method == 'POST':
            room_name = request.form['room_name']
            room_password = request.form['room_password']
            room_id = request.form['room_id']
        return render_template('join_room.jinja2')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
