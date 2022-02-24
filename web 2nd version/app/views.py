import pandas as pd
import numpy as np
import pymysql
import json
from app import app
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify, Blueprint
from app.models import User, GenderEnum, Prediction, LanzhouPre
from werkzeug.security import generate_password_hash
from exts import db
from .forms import LoginForm, RecordForm
from functools import wraps
import flask
import os
import joblib
from sklearn.preprocessing import StandardScaler
from werkzeug.utils import secure_filename

data = Blueprint('data', __name__)


# Define the function that the user must log in to access the page
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # find the current user
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(flask.url_for('login'))

    return wrapper


# the homepage of the website
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # obtain the number of users, actors and TV series
    number1 = User.query.count()
    number2 = Prediction.query.count()
    number5 = LanzhouPre.query.count()
    number3 = 506
    number4 = 3960
    # content = Housing.query.all()
    # types = []
    # for data in content:
    #     types.extend(data.type.split('/'))
    # types = list(set(types))
    # context = {
    #     'posts': Housing.query.all()
    # }
    # return render_template("housing_data.html", **context, number1=number1, number2=number2, number3=number3)
    return render_template("index.html", number1=number1, number2=number2, number3=number3, number4=number4,number5=number5)


# the function of user login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("login"):
            return render_template('login.html', return_to=return_to)
        else:
            return render_template('login.html')

    else:
        form = LoginForm(request.form)
        # the condition of the login form is validate
        if form.validate():
            # Get user input data
            telephone = form.telephone.data
            password = form.password.data
            user = User.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                app.logger.info('User: %s want to login', user.username)
                session["user_id"] = user.id
                return jsonify({"code": 200})
            else:
                flash('Wrong phone number or password！Please confirm before logging in', category="error")
                return jsonify(
                    {"code": 400, "message": 'Wrong phone number or password！Please confirm before logging in'})
        else:
            flash('Form input format error', category="error")
            return jsonify({"code": 400, "message": 'Form input format error'})


# the function of user register
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # the condition of the request is get
    if flask.request.method == 'GET':
        # return register webpage
        return render_template('register.html')
    # the condition of the request is post
    else:
        # Get user input data
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        email = request.form.get('email')
        gender = request.form.get('gender')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # Query whether the user's input mobile phone number has been registered
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            # Prompt error message
            flash('The mobile phone number has been registered please change your mobile phone number.',
                  category="error")
            return redirect(flask.url_for('register'))
        else:
            # Prompt error message
            if password1 != password2:
                flash('The two passwords are not the same, please check them before filling in.',
                      category="error")
                return redirect(flask.url_for('register'))
            elif telephone == '' or username == '' or password1 == '' or password2 == '':
                flash('All information must be filled in.', category="error")
                return redirect(flask.url_for('register'))
            elif len(telephone) != 11:
                flash('telephone length must be 11.', category="error")
                return redirect(flask.url_for('register'))
            # the condition of all information is validate
            else:
                # add the user to the user table
                a = gender
                if gender == 1:
                    a = GenderEnum.MALE
                if gender == 2:
                    a = GenderEnum.FEMALE
                if gender == 3:
                    a = GenderEnum.SECRET
                user = User(telephone=telephone, username=username, password=password1, email=email)
                user.gender = a
                db.session.add(user)
                db.session.commit()
                app.logger.info('User: %s email %s registered successfully', user.username, user.email)
                return redirect(flask.url_for('login'))


@app.context_processor
def context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    # Clear user information in the session
    flask.session.clear()
    return redirect(flask.url_for('login'))


# the function of show user profile
@app.route('/profile/', methods=['GET'])
@login_required
def profile():
    # find the current user
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


# the function of add user profile
@app.route('/add_profile/', methods=['GET', 'POST'])
@login_required
def add_profile():
    if flask.request.method == 'GET':
        return render_template('add_profile.html')
    else:
        # Get user input data
        # try:
        introduce = request.form.get('introduce')
        f = request.files['image_Photo']
        # Path of current file
        basepath = os.path.dirname(__file__)
        # Note: If there is no folder, you must create it first, or you will be prompted that there is no such path
        upload_path = os.path.join(basepath, 'static/uploads/portrait',
                                   secure_filename(f.filename))
        f.save(upload_path)
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.image = f.filename
        user.introduce = introduce
        db.session.add(user)
        db.session.commit()
        app.logger.info('ID: %d  User: %s perfected his portrait', user.id, user.username)
        return redirect(flask.url_for('profile'))


# the function of show all TV series
@app.route('/housing/', methods=['GET', 'POST'])
@login_required
def housing():
    # housing = db.session.query(Housing)
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM housing limit 0,50"
    cur.execute(sql)
    h = cur.fetchall()
    conn.close()
    return render_template('housing_data.html', h=h)


@app.route('/lanzhou_housing/', methods=['GET', 'POST'])
@login_required
def lanzhou_housing():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM lanzhou_housing limit 0,50"
    cur.execute(sql)
    lh = cur.fetchall()
    conn.close()
    return render_template('lanzhou_housing_data.html', lh=lh)


# the function of show all TV series
# @app.route('/chart/', methods=['GET'])
# @login_required
# def chart():
#     return render_template('chart.html')


@app.route('/chart/', methods=['GET', 'POST'])
@login_required
def chart():
    if flask.request.method == 'GET':
        return render_template('chart.html')
    else:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
        cur = conn.cursor()
        sql = "SELECT ID, MEDV FROM housing limit 0,50"
        cur.execute(sql)
        data = [list(x) for x in cur.fetchall()]
        conn.close()
        print(data)
        return json.dumps(data)


@app.route('/chart2/', methods=['POST'])
@login_required
def chart2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT ID, y_test FROM real_predicted"
    cur.execute(sql)
    array1 = [list(x) for x in cur.fetchall()]
    data = ([array1])
    sql2 = "SELECT ID, prediction FROM real_predicted"
    cur.execute(sql2)
    array2 = [list(x) for x in cur.fetchall()]
    print(array2)
    data.insert(1, array2)
    conn.close()
    print(data)
    return json.dumps(data)


@app.route('/lanzhou_chart/', methods=['GET', 'POST'])
@login_required
def lanzhou_chart():
    if flask.request.method == 'GET':
        return render_template('lanzhou_chart.html')
    else:
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='gb2312')
        cur = conn.cursor()
        sql1 = "SELECT COUNT(furnish) FROM lanzhou_housing  WHERE furnish='毛坯' group by district"
        cur.execute(sql1)
        array1 = [list(x) for x in cur.fetchall()]
        array11 = [0, 0, 0, 0, 0, 0]
        array11[0] = array1[0][0]
        array11[1] = array1[1][0]
        array11[2] = array1[2][0]
        array11[3] = array1[3][0]
        array11[4] = array1[4][0]
        array11[5] = array1[5][0]
        # 城关 安宁 七里河 西固 榆中 永登'
        data = ([array11])
        sql2 = "SELECT COUNT(furnish) FROM lanzhou_housing  WHERE furnish='简装修' group by district"
        cur.execute(sql2)
        array2 = [list(x) for x in cur.fetchall()]
        # 城关 七里河 安宁 西固 永登
        array22 = [0, 0, 0, 0, 0, 0]
        array22[0] = array2[0]
        array22[1] = array2[2]
        array22[2] = array2[1]
        array22[3] = array2[3]
        array22[4] = [0]
        array22[5] = array2[4]
        array222 = [0, 0, 0, 0, 0, 0]
        array222[0] = array22[0][0]
        array222[1] = array22[1][0]
        array222[2] = array22[2][0]
        array222[3] = array22[3][0]
        array222[4] = array22[4][0]
        array222[5] = array22[5][0]
        data.insert(1, array222)
        sql3 = "SELECT COUNT(furnish) FROM lanzhou_housing  WHERE furnish='精装修' group by district"
        cur.execute(sql3)
        array3 = [list(x) for x in cur.fetchall()]
        # 安宁 城关 七里河 榆中 西固 永登
        array33 = [0, 0, 0, 0, 0, 0]
        array33[0] = array3[1]
        array33[1] = array3[0]
        array33[2] = array3[2]
        array33[3] = array3[4]
        array33[4] = array3[3]
        array33[5] = array3[5]
        array333 = [0, 0, 0, 0, 0, 0]
        array333[0] = array33[0][0]
        array333[1] = array33[1][0]
        array333[2] = array33[2][0]
        array333[3] = array33[3][0]
        array333[4] = array33[4][0]
        array333[5] = array33[5][0]
        data.insert(2, array333)
        sql4 = "SELECT COUNT(furnish) FROM lanzhou_housing  WHERE furnish='中装修' group by district"
        cur.execute(sql4)
        array4 = [list(x) for x in cur.fetchall()]
        # 安宁 城关 七里河 西固
        array44 = [0, 0, 0, 0, 0, 0]
        array44[0] = array4[1]
        array44[1] = array4[0]
        array44[2] = array4[2]
        array44[3] = array4[3]
        array44[4] = [0]
        array44[5] = [0]
        array444 = [0, 0, 0, 0, 0, 0]
        array444[0] = array44[0][0]
        array444[1] = array44[1][0]
        array444[2] = array44[2][0]
        array444[3] = array44[3][0]
        array444[4] = array44[4][0]
        array444[5] = array44[5][0]
        data.insert(3, array444)
        sql5 = "SELECT COUNT(furnish) FROM lanzhou_housing  WHERE furnish='豪华装修' group by district"
        cur.execute(sql5)
        array5 = [list(x) for x in cur.fetchall()]
        array55 = [0, 0, 0, 0, 0, 0]
        array55[0] = array5[0]
        array55[1] = array5[3]
        array55[2] = array5[2]
        array55[3] = [0]
        array55[4] = array5[1]
        array55[5] = [0]
        array555 = [0, 0, 0, 0, 0, 0]
        array555[0] = array55[0][0]
        array555[1] = array55[1][0]
        array555[2] = array55[2][0]
        array555[3] = array55[3][0]
        array555[4] = array55[4][0]
        array555[5] = array55[5][0]
        # 城关 榆中 七里河 安宁
        data.insert(4, array555)
        print(data)
        print(data[0])
        print(data[1])
        print(data[2])
        print(data[3])
        print(data[4])
        conn.close()
        return json.dumps(data)


@app.route('/lanzhou_chart2/', methods=['GET', 'POST'])
@login_required
def lanzhou_chart2():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='gb2312')
    cur = conn.cursor()
    sql = "SELECT id, price FROM lanzhou_housing limit 0,50"
    cur.execute(sql)
    data = [list(x) for x in cur.fetchall()]
    conn.close()
    print(data)
    return json.dumps(data)


@app.route('/lanzhou_chart3/', methods=['POST'])
@login_required
def lanzhou_chart3():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id, y_test FROM real_predicted2 limit 100,200"
    cur.execute(sql)
    array1 = [list(x) for x in cur.fetchall()]
    data = ([array1])
    sql2 = "SELECT id, prediction FROM real_predicted2 limit 100,200"
    cur.execute(sql2)
    array2 = [list(x) for x in cur.fetchall()]
    print(array2)
    data.insert(1, array2)
    conn.close()
    print(data)
    return json.dumps(data)


# the function of add a TV series
@app.route('/add_prediction/', methods=['GET', 'POST'])
@login_required
def add_prediction():
    if flask.request.method == 'GET':
        return render_template('add_prediction.html')
    else:
        # Get user input data
        CRIM = request.form.get('CRIM')
        ZN = request.form.get('ZN')
        INDUS = request.form.get('INDUS')
        CHAS = request.form.get('CHAS')
        NOX = request.form.get('NOX')
        RM = request.form.get('RM')
        AGE = request.form.get('AGE')
        DIS = request.form.get('DIS')
        RAD = request.form.get('RAD')
        TAX = request.form.get('TAX')
        PTRATIO = request.form.get('PTRATIO')
        B = request.form.get('B')
        LSTAT = request.form.get('LSTAT')
        prediction_array = ([[CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, B, LSTAT]])
        print(prediction_array)
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM housing limit 404,506"
        cur.execute(sql)
        test = cur.fetchall()
        conn.close()
        print(test)
        for i in range(0, 102):
            test_array = [test[i][1], test[i][2], test[i][3], test[i][4], test[i][5], test[i][6], test[i][7],
                          test[i][8], test[i][9], test[i][10], test[i][11], test[i][12], test[i][13]]
            prediction_array.append(test_array)
        print(prediction_array)
        basepath = os.path.dirname(__file__)
        # Note: If there is no folder, you must create it first, or you will be prompted that there is no such path
        upload_path = os.path.join(basepath, 'test.pkl')
        estimator = joblib.load(upload_path)
        transfer = StandardScaler()
        prediction_array = transfer.fit_transform(prediction_array)
        predict_y = estimator.predict(prediction_array)
        MEDV = predict_y[0]
        prediction = Prediction(CRIM=CRIM, ZN=ZN, INDUS=INDUS, CHAS=CHAS, NOX=NOX, RM=RM, AGE=AGE,
                                DIS=DIS, RAD=RAD, TAX=TAX, PTRATIO=PTRATIO, B=B, LSTAT=LSTAT)
        prediction.MEDV = MEDV
        db.session.add(prediction)
        db.session.commit()
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        app.logger.info('ID: %d  User: %s add a prediction ID: %d', user.id, user.username, prediction.id)
        return render_template('prediction_result.html', CRIM=CRIM, ZN=ZN, INDUS=INDUS, CHAS=CHAS, NOX=NOX, RM=RM,
                               AGE=AGE, DIS=DIS, RAD=RAD, TAX=TAX, PTRATIO=PTRATIO, B=B, LSTAT=LSTAT, MEDV=MEDV)


@app.route('/lanzhou_add_prediction/', methods=['GET', 'POST'])
@login_required
def lanzhou_add_prediction():
    if flask.request.method == 'GET':
        return render_template('lanzhou_add_prediction.html')
    else:
        # Get user input data
        district = request.form.get('district')
        furnish = request.form.get('furnish')
        facing = request.form.get('facing')
        floor = request.form.get('floor')
        room = request.form.get('room')
        hall = request.form.get('hall')
        elevator = request.form.get('elevator')
        bui_category = request.form.get('bui_category')
        property = request.form.get('property')
        school = request.form.get('school')
        year = request.form.get('year')
        area = request.form.get('area')
        prediction_array = ([[district, furnish, facing, floor, room, hall, elevator, bui_category, property, school,
                              area, year]])
        print(prediction_array)
        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
        cur = conn.cursor()
        sql = "SELECT * FROM lanzhou_test"
        cur.execute(sql)
        test = cur.fetchall()
        conn.close()
        print(test)
        for i in range(0, 792):
            test_array = [test[i][1], test[i][2], test[i][3], test[i][4], test[i][5], test[i][6], test[i][7],
                          test[i][8], test[i][9], test[i][10], test[i][11], test[i][12]]
            prediction_array.append(test_array)
        print(prediction_array)
        columns1 = ['district', 'furnish', 'facing', 'floor', 'room', 'hall', 'elevator', 'bui_category', 'property',
                    'school', 'area', 'year']
        df = pd.DataFrame(prediction_array, columns=columns1)
        district_map = {'永登': 1, '榆中': 2, '西固': 3, '七里河': 4, '安宁': 5, '城关': 6}
        furnish_map = {'毛坯': 1, '简装修': 2, '精装修': 3, '中装修': 4, '豪华装修': 5}
        facing_map = {'北': 1, '东': 2, '西': 3, '东西': 4, '南': 5, '南北': 6, '西北': 7, '东北': 8, '东南': 9, '西南': 10}
        floor_map = {'低': 1, '中': 2, '高': 3}
        elevator_map = {'无': 0, '有': 1, '无 ': 0, '有 ': 1}
        bui_category_map = {'砖混': 1, '砖楼': 2, '塔板结合': 3, '板楼': 4, '钢混': 5, '平房': 6, '塔楼': 7}
        property_map = {'房本房': 1, '经济适用房': 2, '房改房': 3, '普通商品房': 4, '个人产权': 5, '商品房': 6, '商品房(免税)': 7, '限价房': 8}
        df['district'] = df['district'].map(district_map)
        df['furnish'] = df['furnish'].map(furnish_map)
        df['facing'] = df['facing'].map(facing_map)
        df['floor'] = df['floor'].map(floor_map)
        df['elevator'] = df['elevator'].map(elevator_map)
        df['bui_category'] = df['bui_category'].map(bui_category_map)
        df['property'] = df['property'].map(property_map)
        df['year'] = df['year'].astype('int32')
        df['age'] = df['year'].map(lambda x: 2022 - x)
        df.drop(columns=['year'], inplace=True)
        prediction_array = df.values
        print(prediction_array[2])
        basepath = os.path.dirname(__file__)
        # Note: If there is no folder, you must create it first, or you will be prompted that there is no such path
        upload_path = os.path.join(basepath, 'gb_reg.pkl')
        estimator = joblib.load(upload_path)
        transfer = StandardScaler()
        prediction_array = transfer.fit_transform(prediction_array)
        predict_y = np.expm1(estimator.predict(prediction_array))
        price = predict_y[0]
        lanzhou_pre = LanzhouPre(district=district, furnish=furnish, facing=facing, floor=floor, room=room, hall=hall,
                                 elevator=elevator, bui_category=bui_category, property=property, school=school,
                                 year=year, area=area)
        lanzhou_pre.price = price
        db.session.add(lanzhou_pre)
        db.session.commit()
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        app.logger.info('ID: %d  User: %s add a prediction ID: %d', user.id, user.username, lanzhou_pre.id)
        return render_template('lanzhou_pre_result.html', district=district, furnish=furnish, facing=facing,
                               floor=floor, room=room, hall=hall, elevator=elevator, bui_category=bui_category,
                               property=property, school=school, year=year, area=area, price=price)


# the function of show all watching records
@app.route('/prediction/', methods=['GET', 'POST'])
@login_required
def prediction():
    # find the current user
    # user_id = session.get('user_id')
    # user = User.query.get(user_id)
    prediction = Prediction.query.all()
    preCurrent = []
    for pre in prediction:
        preCurrent.append(pre)
    return render_template('prediction_record.html', record=preCurrent)


@app.route('/lanzhuo_prediction/', methods=['GET', 'POST'])
@login_required
def lanzhou_prediction():
    # find the current user
    # user_id = session.get('user_id')
    # user = User.query.get(user_id)
    lanzhou_prediction = LanzhouPre.query.all()
    preCurrent = []
    for pre in lanzhou_prediction:
        preCurrent.append(pre)
    return render_template('lanzhou_pre_record.html', record=preCurrent)


# the function of change user password
@app.route('/alter_passwd/', methods=['GET', 'POST'])
@login_required
def alter_passwd():
    if flask.request.method == 'GET':
        return render_template('change_passwd.html')
    else:
        # Get user input data
        passwd1 = request.form.get('passwd1')
        passwd2 = request.form.get('passwd2')
        if passwd1 != passwd2:
            return jsonify(
                {"code": 404, "message": "The two passwords are not the same, please check them before filling in"})
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.password = generate_password_hash(passwd1)
        db.session.add(user)
        db.session.commit()
        app.logger.info('ID: %d  User: %s change password to %s', user.id, user.username, passwd1)
        return jsonify({"code": 200})


# the function of change user email
@app.route('/alter_email/', methods=['GET', 'POST'])
@login_required
def alter_email():
    if flask.request.method == 'GET':
        return render_template('change_email.html')
    else:
        # Get user input data
        email = request.form.get('email')
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.email = email
        db.session.add(user)
        db.session.commit()
        app.logger.info('ID: %d  User: %s change email to %s', user.id, user.username, email)
        return jsonify({"code": 200})


# the function of change username
@app.route('/alter_username/', methods=['GET', 'POST'])
@login_required
def alter_username():
    if flask.request.method == 'GET':
        return render_template('change_username.html')
    else:
        # Get user input data
        username = request.form.get('username')
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user.username = username
        db.session.add(user)
        db.session.commit()
        app.logger.info('ID: %d  User: %s change username to %s', user.id, user.username, username)
        return jsonify({"code": 200})


# the function of query TV series according to type and area
# @app.route("/query", methods=['GET', 'POST'])
# def query():
#     # obtain the number of users, actors and TV series
#     number1 = User.query.count()
#     number2 = Actor.query.count()
#     number3 = TV.query.count()
#     content = TV.query.all()
#     area = request.values.get('area')
#     type = request.values.get('type')
#     tv_areas = []
#     tv_types = []
#     if area != 'all':
#         tv_areas.append(area)
#         content = TV.query.filter(TV.area.in_(tv_areas))
#         content = [tv for tv in content if tv.area in tv_areas]
#     if type != 'all':
#         tv_types.append(type)
#         content = TV.query.filter(TV.type.in_(tv_types))
#     context = {
#         'posts': content
#     }
#     return render_template("index.html", **context, number1=number1, number2=number2, number3=number3, type=type,
#                            area=area)


# the function of delete a TV series
# @app.route('/deleteRecord/', methods=['GET', 'POST'])
# @login_required
# def deleteRecord():
#     message = ''
#     id = request.args.get("id")
#     user_id = session.get('user_id')
#     try:
#         old = Prediction.query.get(id)
#         db.session.delete(old)
#         db.session.commit()
#     except:
#         db.session.rollback()
#         message = 'this tv has tv-record can not delete'
#         pass
#     tv = db.session.query(TV)
#     return render_template('housing_data.html', tv=tv, message=message)


# the function of delete a TV series record
@app.route('/deleteRe/', methods=['GET', 'POST'])
@login_required
def deleteRe():
    id = request.args.get("id")
    try:
        old = Prediction.query.get(id)
        db.session.delete(old)
        db.session.commit()
    except:
        db.session.rollback()
    record = db.session.query(Prediction)
    return render_template('prediction_record.html', record=record)


@app.route('/deleteLanRe/', methods=['GET', 'POST'])
@login_required
def deleteLanRe():
    id = request.args.get("id")
    try:
        old = LanzhouPre.query.get(id)
        db.session.delete(old)
        db.session.commit()
    except:
        db.session.rollback()
    record = db.session.query(LanzhouPre)
    return render_template('lanzhou_pre_record.html', record=record)

# Display a record list containing keywords
# @app.route('/search_record/')
# @login_required
# def search_record():
#     # Get keywords entered by the user
#     q = flask.request.args.get('q')
#     content = TV.name
#     # Query Tv series name that contain keywords entered by the user
#     tv = TV.query.filter(content.contains(q))
#     return flask.render_template('housing_data.html', tv=tv)


# edit record information function
# @app.route('/edit_record/<id>', methods=['GET', 'POST'])
# @login_required
# def edit_record(id):
#     # the condition of the request is get
#     if flask.request.method == 'GET':
#         record = TVRecord.query.get(id)
#         form = RecordForm(obj=record)
#         # return edit record webpage
#         return render_template('edit_record.html', form=form)
#     # the condition of the request is post
#     else:
#         # Get the record to be edited
#         record = TVRecord.query.get(id)
#         # Get form information entered by the user
#         form = RecordForm(flask.request.form)
#         # All data fields have been filled
#         if form.validate():
#             # Modify record information
#             r = record
#             r.score = form.score.data
#             r.view_time = form.view_time.data
#             r.content = form.content.data
#             db.session.commit()
#             # return all records page
#             return redirect(flask.url_for('record'))
#         # Prompt error message
#         else:
#             flash('All fields must be filled in.', category="error")
#             return redirect(flask.url_for('edit_record'))
