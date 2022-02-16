import pymysql
import json
from app import app
from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify, Blueprint
from app.models import User, GenderEnum, Prediction
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
    number3 = Prediction.query.count()
    number2 = 506
    # content = Housing.query.all()
    # types = []
    # for data in content:
    #     types.extend(data.type.split('/'))
    # types = list(set(types))
    # context = {
    #     'posts': Housing.query.all()
    # }
    # return render_template("housing_data.html", **context, number1=number1, number2=number2, number3=number3)
    return render_template("index.html", number1=number1, number2=number2, number3=number3)


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


# the function of show all TV series
@app.route('/chart/', methods=['GET'])
@login_required
def chart():
    return render_template('chart.html')


@app.route('/chart/', methods=['POST'])
@login_required
def chart_data():
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
def chart_data2():
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


# @app.route('/chart/', methods=['POST'])
# @login_required
# def chart_data2():
#     conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
#     cur = conn.cursor()
#     sql = "SELECT ID, y_test FROM real_predicted"
#     cur.execute(sql)
#     array = [list(x) for x in cur.fetchall()]
#     print(array)
#     data = ([array])
#     print(data)
#     cur1 = conn.cursor()
#     sql1 = "SELECT ID, y_test FROM real_predicted"
#     cur1.execute(sql1)
#     array1 = [list(x) for x in cur1.fetchall()]
#     data.insert(1, array1)
#     conn.close()
#     print(data)
#     return json.dumps(data)


#     data = db.session.query(housing).all()
#     view_data = {}
#     view_data["id"] = []
#     view_data["price"] = []
#
#     def build_view_data(item):
#         view_data["id"].append(item.id)
#         view_data["price"].append(item.MEDV)
#
#     [build_view_data(item) for item in data]
#
#     return json.dumps(view_data, ensure_ascii=False)
# housing = db.session.query(Housing)
# conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='housing', charset='utf8')
# cur = conn.cursor()
# sql = "SELECT MEDV FROM housing limit 0,50"
# cur.execute(sql)
# price = cur.fetchall()
# conn.close()

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


# the function of add a TV series watching record
# @app.route('/add_record/', methods=['GET', 'POST'])
# @login_required
# def add_record():
#     if flask.request.method == 'GET':
#         tv = TV.query.filter()
#         return render_template('add_record.html', tv=tv)
#     else:
#         # Get user input data
#         tv = request.form.get('tv')
#         score = request.form.get('score')
#         view_time = request.form.get('view_time')
#         content = request.form.get('content')
#         re = TVRecord(tv_id=tv, score=score, view_time=view_time, content=content)
#         user_id = session.get('user_id')
#         user = User.query.get(user_id)
#         re.users.append(user)
#         db.session.add(re)
#         db.session.commit()
#         app.logger.info('ID: %d  User: %s add a TV watching record of tv ID: %d', user.id, user.username, re.tv_id)
#         return jsonify({"code": 200})


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
