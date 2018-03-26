from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
# 创建栏目表
class Navigation(db.Model):
    __tablename__ ='navigation'
    navId = db.Column(db.Integer,primary_key=True,autoincrement=True)
    navName = db.Column(db.String(20))
# 创建菜单表
class Menu(db.Model):
    __tablename__ = 'menu'
    mId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mName = db.Column(db.String(20))
    link = db.Column(db.String(50))
    navId = db.Column(db.Integer,db.ForeignKey('navigation.navId'))
# 创建文章表
class Article(db.Model):
    __tablename__ = 'article'
    aId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    src = db.Column(db.String(100))
    time = db.Column(db.Date)
    mId = db.Column(db.Integer,db.ForeignKey('menu.mId'))
# 创建评论表
class Comment(db.Model):
    __tablename__ = 'comment'
    cId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uId = db.Column(db.Integer, db.ForeignKey('user.uId'))
    aId = db.Column(db.Integer, db.ForeignKey('article.aId'))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.datetime.now)

# 创建用户表
class User(db.Model):
    __tablename__ = 'user'
    uId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        email = kwargs.get('email')
        username = kwargs.get('username')
        password = kwargs.get('password')
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
    def check_password(self, raw_password):
        result = check_password_hash(self.password,raw_password)
        return result





