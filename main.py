#-*- coding: utf-8 -*-
from flask import Flask, url_for, request, render_template, redirect, session
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from registerform import RegisterForm
from loginform import LoginForm
from add_dish import AddDishForm
from dishmodel import DishModel
from usersmodel import UsersModel
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db = DB()
UsersModel(db.get_connection()).init_table()
DishModel(db.get_connection()).init_table()

@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return render_template('homepage.html')
    dish = DishModel(db.get_connection()).get_all()
    return render_template('index.html', username=session['username'], dish = dish)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect("/index")
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/index")
        else:
            return render_template('login.html', form=form, message=exists[1])
    # print(UsersModel(db.get_connection()).exists(form.username.data, form.password.data))
    return render_template('login.html', form=form, message="")


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/homepage')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form, message="")
    elif request.method == 'POST':
        if form.password.data != form.trypassword.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        if user_model.get_by_name(user_name) is None:
            user_model.insert(user_name, password)
            exists = user_model.exists(user_name, password)
            return redirect("/login")
        else:
            return render_template('register.html', form=form, message="Такой пользователь уже есть. Исправьте данные")

        """
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")"""

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if 'username' not in session:
        return redirect('/login')
    form = AddDishForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        dish = DishModel(db.get_connection())
        dish.insert(title, content, session['user_id'])
        return redirect("/index")
    return render_template('add_dish.html', title='Рецепты',
                           form=form, username=session['username'])

@app.route('/delete_recipe/<int:dish_id>', methods=['GET'])
def delete_dish(dish_id):
    if 'username' not in session:
        return redirect('/login')
    nm = DishModel(db.get_connection())
    nm.delete(dish_id)
    return redirect("/index")

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')