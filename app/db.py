from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True) # user id
    name = Column(String) # prefer user name
    email = Column(String, unique=True) # mail@mail.com
    password = Column(String) # Password hashed
    is_active = Column(Boolean, default=True)
    # status = Column(String) # Online/ofline
    last_login = Column(DateTime) # Последний раз был в сети только что
    chat_settings_id = Column(Integer, ForeignKey('chat_settings.id')) # Настройки чата
    
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True) # message id
    text = Column(String) # message text
    user_from = Column(Integer) # user id
    user_to = Column(Integer) # user id
    timestamp = Column(DateTime) # время отправки message
    
    
# Онлайн-участники (online_users): - список пользователей, которые в данный момент онлайн 
class OnlineUser(Base):
    __tablename__ = 'online_users'
    
    id = Column(Integer, primary_key=True)
    # Add any additional columns as needed

# параметры чата, такие как имя, описание, аватар и т.д.
class ChatSettings(Base):
    __tablename__ = 'chat_settings'
    
    id = Column(Integer, primary_key=True)
    background = Column(String)
    avatar = Column(String)
    # Add any additional columns as needed


# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()