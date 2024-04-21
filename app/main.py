    # create the avatar #
# chat_settings = ChatSettings()
# chat_settings.avatar = image_data
from flask import Flask, jsonify, request
from db import Session, User, OnlineUser, ChatSettings, Message
from sqlalchemy import insert
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime as date
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# session = Session()
DB = SQLAlchemy(app)

# app.secret_key = '3131eg43'

# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return DB.session.query(User).get(user_id)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    response.headers['Access-Control-Allow-Methods'] = 'DELETE'
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
            'status': user.is_active
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
        user_data_m = DB.session.query(User).filter_by(email=user, password=password).first()
        
        def checkUser(user_data, user_data_m):
            if user_data is None:
                return user_data_m
            if user_data_m is None:
                return None
            else:
                return user_data
            
        user_dt = checkUser(user_data=user_data, user_data_m=user_data_m)
        
        if user_dt is None:
            return jsonify({'message': 'Ошибка запроса: пользователь не найден'})
        
        user_dict = {
            'id': user_dt.id,
            'name': user_dt.name,
            'email': user_dt.email,
        }
        # login_user(user_dt)
        return jsonify(user_dict)
    else:
        return 'Ошибка запроса метода, кроме запроса на создание пользователя'



@app.route('/profile/<int:id>', methods=['POST', 'GET'])
def profile():
    if request.method == 'POST':
        user = (request.get_json().get('name'))
        # password = generate_password_hash(request.get_json().get('password'))
        user_data = DB.session.query(User).filter_by(name=user).first()
        if user_data is None:
            return 'Ошибка запроса: пользователь не найден'
        user_dict = {
            'id': user_data.id,
            'name': user_data.name,
            'email': user_data.email
        }
        return jsonify(user_dict)
    else:
        return 'Ошибка запроса метода, кроме запроса на создание пользователя'


# 
@app.route('/messages', methods=['GET', 'POST'])
def get_messages():
    # if current_user.is_authenticated:
        
        # POFIXI MENYA
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
    # else:
    #     return jsonify({'message': 'User is not authenticated'})


# post messages
@app.route('/sendmsg', methods=['POST'])
def send_msg():
    userfrom = request.get_json().get()['user_from']
    userto = request.get_json().get()['user_to']
    text = request.get_json().get('text')  # Исправлено
    message = Message(text=text, user_from=userfrom, user_to=userto, timestamp=date.datetime.now())
    DB.session.add(message)
    DB.session.commit()
    return 'Message received and added to the database.'

@app.route('/editmsg/<int:id>', methods=['POST'])
def edit_msg(id):
    # id = request.get_json()[int('id')]
    text = request.get_json()['text']
    message = DB.session.query(Message).filter_by(id=id).first()
    message.text = text
    DB.session.commit()
    return 'message succesful updated'



@app.route('/delmsg/<int:id>', methods=['DELETE'])
def delete_msg(id):
    # id = request.get_json()[int('id')]
    message = DB.session.query(Message).filter_by(id=id).first()
    DB.session.delete(message)
    DB.session.commit()
    return 'message succesful deleted.'

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
        DB.create_all()
        # login_manager.user_loader(load_user)  # Добавить эту строку
        app.run(debug=True)
