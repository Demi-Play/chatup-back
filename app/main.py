    # create the avatar #
# chat_settings = ChatSettings()
# chat_settings.avatar = image_data
from flask import Flask, jsonify, render_template, request
from db import Session, User, OnlineUser, ChatSettings, Message
from sqlalchemy import insert
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime as date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# session = Session()
DB = SQLAlchemy(app)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response


# user
@app.route('/users')
def get_users():
    users = DB.session.query(User).all()
    user_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'status': user.status
        }
        user_list.append(user_dict)
    return jsonify(user_list)


@app.route('/reg', methods=['POST'])
def create_user():
    if request.method == 'POST':
        name = request.get_json().get('name')
        email = request.get_json().get('email')
        password = request.get_json().get('password')
        
        if name and email and password:
            # Проверка наличия пользователя с таким же email
            existing_user = DB.session.query(User).filter_by(email=email, name=name, password=password).first()
            if existing_user:
                return 'Ошибка запроса: пользователь с таким email уже существует'
            user_data = User(name=name, email=email, password=password)
            user_dict = {
            'id': user_data.id,
            'name': user_data.name,
            'email': user_data.email,
        }
            DB.session.add(user_data)
            DB.session.commit()
            return jsonify(user_dict)
        else:
            return 'Ошибка запроса: не все поля заполнены'
    else:
        return 'Ошибка запроса метода, кроме запроса на создание пользователя'
    

@app.route('/auth', methods=['POST'])
def auth_user():
    if request.method == 'POST':
        user = request.get_json().get('name')
        password = request.get_json().get('password')
        user_data = DB.session.query(User).filter_by(name=user, password=password).first()
        if user_data is None:
            return 'Ошибка запроса: пользователь не найден'
        
        user_dict = {
            'id': user_data.id,
            'name': user_data.name,
            'email': user_data.email,
        }
    
    else:
        return 'Ошибка запроса метода, кроме запроса на создание пользователя'
    return jsonify(user_dict)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        user = request.get_json()['name']
        password = request.get_json()['password']
        user_data = DB.session.query(User).filter_by(name=user, password=password).first()
        if user_data is None:
            return 'Ошибка запроса: пользователь не найден'
        user_dict = {
            'id': user_data.id,
            'name': user_data.name,
            'email': user_data.email,
            'password': user_data.password,
        }
        return jsonify(user_dict)
    else:
        return 'Ошибка запроса метода, кроме запроса на создание пользователя'


# 
@app.route('/messages')
def get_messages():
    messages = DB.session.query(Message).all()
    message_list = []
    for message in messages:
        message_dict = {
            'id': message.id,
            'text': message.text,
            'user_from': message.user_from,
            'user_to': message.user_to,
            'timestamp': message.timestamp
        }
        message_list.append(message_dict)
    return jsonify(message_list)

# post messages
@app.route('/sendmsg', methods=['POST', 'GET'])
def send_msg():
    userfrom = request.get_json()['user_from']
    userto = request.get_json()['user_to']
    text = request.form.get('text')  # Исправлено
    message = Message(text=text, user_from=userfrom, user_to=userto, timestamp=date.datetime.now())
    DB.session.add(message)
    DB.session.commit()
    return 'Message received and added to the database.'



#  
@app.route('/online_users')
def get_online_users():
    online_users = DB.session.query(OnlineUser).all()
    online_user_list = []
    for online_user in online_users:
        online_user_dict = {
            'id': online_user.id
        }
        online_user_list.append(online_user_dict)
    return jsonify(online_user_list)

# 
@app.route('/chat_settings')
def get_chat_settings():
    chat_settings = DB.session.query(ChatSettings).all()
    chat_settings_list = []
    for chat_setting in chat_settings:
        chat_setting_dict = {
            'id': chat_setting.id,
            'background': chat_setting.background,
            'avatar': chat_setting.avatar
        }
        chat_settings_list.append(chat_setting_dict)
    return jsonify(chat_settings_list)

if __name__ == '__main__':
    with app.app_context():
        # Весь код, связанный с Flask-приложением, должен быть здесь но как бы нахер надо
        DB.create_all()
        app.run(debug=True)