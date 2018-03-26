from flask import Flask,render_template, g, request, jsonify, redirect, url_for, session
from models import Navigation, Menu, Article, User, Comment
from exts import db
import config, re, random
from zd import content_main
from laod import laod_news
from sqlalchemy import or_, func
app = Flask(__name__)
app.config.from_object(config)
app.secret_key = 'super secret key'
db.init_app(app)

@app.context_processor
def load_nav():
    # 一级菜单参数
    navName = db.session.query(Navigation.navName,Navigation.navId).all()
    # 二级菜单参数
    mName = db.session.query(Menu.mName,Menu.navId,Menu.link).all()
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.uId == user_id).first()
    else:
        user = None
    context = {
        'user': user,
        'navname': navName,
        'mname': mName,
        're': re,
        'str': str
    }
    return {**context}
    # return {'': navName,'mname': mName}

@app.route('/')
def hello_world():
    # # 增加栏目
    #
    # addNav = ([Navigation(navName='资源分享'),
    #            Navigation(navName='最新资讯'),
    #            Navigation(navName='精美图片')])
    # db.session.add_all(addNav)
    # db.session.commit()
    # # 增加栏目菜单
    # addMenu = ([Menu(mName='媒体播放', navId=1, link='/media/'),
    #             Menu(mName='办公软件', navId=1, link='/office/'),
    #             Menu(mName='网页浏览', navId=1, link='/browse/'),
    #             Menu(mName='游戏娱乐', navId=1, link='/game/'),
    #             Menu(mName='科技资讯', navId=2, link='/technology/'),
    #             Menu(mName='热点资讯', navId=2, link='/hotspot/'),
    #             Menu(mName='妹子图', navId=3, link='/mmfigure/')])
    # db.session.add_all(addMenu)
    # db.session.commit()

    # 查询栏目表 (一级菜单)
    # select navName from navigation

    # 传参到 base.html
    software = db.session.query(Article.content, Article.aId, Article.title, Article.time, Menu.mName).filter(
        Navigation.navId == 1,Article.mId == Menu.mId,Menu.navId==Navigation.navId) \
        .order_by(-Article.time).limit(15)
    news = db.session.query(Article.content, Article.aId, Article.title, Article.time, Menu.mName).filter(
        Navigation.navId == 2,Article.mId == Menu.mId,Menu.navId==Navigation.navId) \
        .order_by(-Article.time).limit(15)
    newcomment = db.session.query(Comment.content,User.username,Comment.aId,Comment.time).filter(Comment.uId==User.uId)\
        .order_by(-Comment.time).limit(15)
    return render_template('index.html', software=software,news=news, newcomment=newcomment)
@app.route('/randomart/')
def RandomArt():
    count = db.session.query(func.count(Article.aId)).scalar()
    mit = random.randint(1, count-10)
    randomart = db.session.query(Article.aId, Article.title, Article.time) \
        .order_by(-Article.time).limit(10).offset(mit).all()
    return jsonify({'randomart': randomart, 'verify': 'success'})

@app.route('/showcontent/')
def ShowContent():
    # # 增加栏目
    #
    # addNav = ([Navigation(navName='资源分享'),
    #            Navigation(navName='最新资讯'),
    #            Navigation(navName='精美图片')])
    # db.session.add_all(addNav)
    # db.session.commit()
    # # 增加栏目菜单
    # addMenu = ([Menu(mName='媒体播放', navId=1, link='/media/'),
    #             Menu(mName='办公软件', navId=1, link='/office/'),
    #             Menu(mName='网页浏览', navId=1, link='/browse/'),
    #             Menu(mName='游戏娱乐', navId=1, link='/game/'),
    #             Menu(mName='科技资讯', navId=2, link='/technology/'),
    #             Menu(mName='热点资讯', navId=2, link='/hotspot/'),
    #             Menu(mName='妹子图', navId=3, link='/mmfigure/')])
    # db.session.add_all(addMenu)
    # db.session.commit()

    # 查询栏目表 (一级菜单)
    # select navName from navigation

    # 传参到 base.html
    aid = int(request.args.get('aid'))
    content = db.session.query(Article.content,Article.title, Article.time).filter(Article.aId == aid).all()
    comment = db.session.query(Comment.content, User.username, Comment.time)\
        .filter(Comment.aId == aid,Comment.aId == Article.aId, Comment.uId == User.uId)\
        .order_by(-Comment.time).all()
    return jsonify({'content': content, 'comment': comment, 'verify': 'success'})

@app.route('/part/<link>')
def Part(link):
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Article.content,Article.aId, Article.title, Article.time, Menu.mName) \
        .filter(Menu.mId == Article.mId, Menu.link==link) \
        .order_by(Article.time.desc()) \
        .paginate(page, per_page=8, error_out=False)
    content = pagination.items
    methname = "Part"
    return render_template('media.html', content=content, pagination=pagination, link=link, methname=methname )

#
# @app.route('/office/')
# def Office():
#     content = db.session.query(Article.content, Article.title, Article.time, Menu.mName).filter(Menu.mId==Article.mId,Article.mId==2) \
#         .order_by(Article.time.desc()).all()
#     return render_template('media.html',content=content)
# @app.route('/browse/')
# def Browse():
#
#
# @app.route('/android/')
# def Android():
#     page = request.args.get('page', 1, type=int)
#     pagination = db.session.query(Article.content, Article.title, Article.time, Menu.mName)\
#         .filter(Menu.mId==Article.mId,Article.mId==8)\
#         .order_by(Article.time.desc())\
#         .paginate(page, per_page=10, error_out=False)
#     content = pagination.items
#     methname = 'Android'
#     return render_template('media.html', methname=methname, content=content, pagination=pagination)
#
# @app.route('/graphic/')
# def Graphic():
#     content = db.session.query(Article.content, Article.title, Article.time, Menu.mName).filter(Menu.mId==Article.mId,Article.mId==10) \
#         .order_by(Article.time.desc()).all()
#     return render_template('media.html',content=content)
# @app.route('/updownload/')
# def UpDownload():
#     content = db.session.query(Article.content, Article.title, Article.time, Menu.mName).filter(Menu.mId==Article.mId,Article.mId==11) \
#         .order_by(Article.time.desc()).all()
#     return render_template('media.html',content=content)
# @app.route('/hotapps/')
# def HotApps():
#     content = db.session.query(Article.content, Article.title, Article.time, Menu.mName).filter(Menu.mId==Article.mId,Article.mId==9) \
#         .order_by(Article.time.desc()).all()
#     return render_template('media.html',content=content)
# @app.route('/game/')
# def Game():
#     content = db.session.query(Article.content, Article.title, Article.time, Menu.mName).filter(Menu.mId==Article.mId,Article.mId==4) \
#         .order_by(Article.time.desc()).all()
#     return render_template('media.html',content=content)
@app.route('/search/')
def Search():
    link = request.args.get('link')
    # content = db.session.query(Article.content, Article.title, Article.time, Menu.mName)\
    #     .filter(Menu.mId==Article.mId, Article.title.ilike('%'+q+'%')).order_by( Article.time.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Article.content, Article.title, Article.time, Menu.mName, Article.aId).filter(Menu.mId == Article.mId) \
        .filter(or_(Article.title.contains(link))).order_by(-Article.time)\
        .paginate(page, per_page=8, error_out=False)
    content = pagination.items
    methname = "Search"

    return render_template('media.html', content=content, pagination=pagination, link=link, methname=methname)
@app.route('/regist/',methods=['GET','POST'])
def Regist():
    if request.method == 'GET':
        return render_template('media.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        # email 验证，如果被注册不能再使用
        user = User.query.filter(User.email == email).first()
        if user:
            return jsonify({'result': 'error', 'verify': 'failed'})
        else:
            user = User(username=username,password=password,email=email)
            db.session.add(user)
            db.session.commit()
            return jsonify({'result': 'success', 'verify': 'success'})
@app.route('/CheckEmail/',methods=['GET','POST'])
def CheckEmail():
    if request.method == 'GET':
        return render_template('media.html')
    else:
        email = request.form.get('email')
        # email 验证，如果被注册不能再使用
        user = User.query.filter(User.email == email).first()

        if user:
            return jsonify({"valid": False})

        else:
            return jsonify({"valid": True})
@app.route('/login/',methods=['GET','POST'])
def Login():
    if request.method == 'GET':
        return render_template('media.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            session['user_id'] = user.uId
            # 如果想在31天内都不需要登录
            session.permanent = True
            return jsonify({'result': 'success', 'verify': 'success'})
        else:
            return jsonify({'result': 'error', 'verify': 'failed'})

    # if request.method == 'GET':
    #     return render_template('media.html')
    # else:
    #     password = request.form.get('password')
    #     email = request.form.get('email')
    #     user = User.query.filter(User.email == email).first()
    #     if user and user.check_password(password):
    #
    #         session['user_id'] = user.uId
    #         # 如果想在31天内都不需要登录
    #         session.permanent = True
    #         return redirect(url_for('hello_world'))
    #     else:
    #         Mes = "邮箱或密码错误！"
    #         print(Mes)
    #         return render_template('media.html', Mes=Mes)
@app.route('/logout/')
def Logout():
    #session.pop('user_id')
    #session.clear()
    if session.get('user_id'):
        del session['user_id']
    return redirect(url_for('hello_world'))
@app.route('/comment/')
def MakeComment():
    if session.get('user_id'):
        uid = session['user_id']
        content = request.args.get('content')
        # aid = int(request.form.get('aId'))
        aid = request.args.get('aid')
        addcomment = Comment(aId=aid, uId=uid, content=content)
        db.session.add(addcomment)
        db.session.commit()
        return jsonify({'result': 'success', 'verify': 'success'})
    else:
        return jsonify({'result': 'error', 'verify': 'failed'})

@app.route('/zd423/')
def loadzd423():
    content_list = content_main()
    print(content_list)
    for cl in content_list:
        print(cl['title'])
        # print(cl['date'])
        # time = datetime.datetime.strptime(cl['date'], '%Y-%m-%d')
        # print(time)
        addContent = ([Article(content=cl['content'], title=cl['title'], src=cl['src'], time=cl['date'], mId=cl['mid'])])
        db.session.add_all(addContent)
        db.session.commit()
    print("抓取zd423完成！")
    return render_template('zd423.html')
@app.route('/laod/')
def loadlaod():
    content_list = laod_news()
    for cl in content_list:

        # print(cl['date'])
        # time = datetime.datetime.strptime(cl['date'], '%Y-%m-%d')
        # print(time)
        addContent = ([Article(content=cl['content'], title=cl['title'],time=cl['date'], src=cl['src'], mId=cl['mid'])])

        db.session.add_all(addContent)

        db.session.commit()


    print("抓取laod完成！")
    return render_template('zd423.html')
if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
