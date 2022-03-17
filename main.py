from flask import Flask, url_for, redirect, render_template, session, flash, request
import mysql.connector
from db_connect import *

app = Flask(__name__, template_folder='templates')
app.secret_key = "marcel"


@app.route('/account')
def account():
    return render_template('account.jinja2')


@app.route('/account-login')
def login():
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
            if cursor.fetchone()[0]:
                flash('username already exist, try other', 'info')
            else:
                username_add_to_db = 'INSERT INTO users (username, password) VALUES(%s, %s)'
                value_username_add_to_db = (username_register, password_register)
                cursor.execute(username_add_to_db, value_username_add_to_db)
                db_connect.commit()
                return redirect(url_for('login'))

    return render_template('register.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
