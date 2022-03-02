from werkzeug.security import check_password_hash, generate_password_hash

from exts import db
import enum
from datetime import datetime


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


# create a database table named User
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False, default=GenderEnum.UNKNOW)
    image = db.Column(db.String(50))
    introduce = db.Column(db.TEXT)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        password = kwargs.pop('password')
        username = kwargs.pop('username')
        telephone = kwargs.pop('telephone')
        email = kwargs.pop('email')
        self.password = generate_password_hash(password)
        self.username = username
        self.telephone = telephone
        self.email = email

    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)


# Create a database table named prediction
class Prediction(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CRIM = db.Column(db.Float, nullable=False)
    ZN = db.Column(db.Float, nullable=False)
    INDUS = db.Column(db.Float, nullable=False)
    CHAS = db.Column(db.Integer, nullable=False)
    NOX = db.Column(db.Float, nullable=False)
    RM = db.Column(db.Float, nullable=False)
    AGE = db.Column(db.Float, nullable=False)
    DIS = db.Column(db.Float, nullable=False)
    RAD = db.Column(db.Float, nullable=False)
    TAX = db.Column(db.Float, nullable=False)
    PTRATIO = db.Column(db.Float, nullable=False)
    B = db.Column(db.Float, nullable=False)
    LSTAT = db.Column(db.Float, nullable=False)
    MEDV = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        CRIM = kwargs.pop('CRIM')
        ZN = kwargs.pop('ZN')
        INDUS = kwargs.pop('INDUS')
        CHAS = kwargs.pop('CHAS')
        NOX = kwargs.pop('NOX')
        RM = kwargs.pop('RM')
        AGE = kwargs.pop('AGE')
        DIS = kwargs.pop('DIS')
        RAD = kwargs.pop('RAD')
        TAX = kwargs.pop('TAX')
        PTRATIO = kwargs.pop('PTRATIO')
        B = kwargs.pop('B')
        LSTAT = kwargs.pop('LSTAT')
        self.CRIM = CRIM
        self.ZN = ZN
        self.INDUS = INDUS
        self.CHAS = CHAS
        self.NOX = NOX
        self.RM = RM
        self.AGE = AGE
        self.DIS = DIS
        self.RAD = RAD
        self.TAX = TAX
        self.PTRATIO = PTRATIO
        self.B = B
        self.LSTAT = LSTAT


# Create a database table named lanzhou_pre
class LanzhouPre(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'lanzhou_pre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    district = db.Column(db.String(10), nullable=False)
    furnish = db.Column(db.String(10), nullable=False)
    facing = db.Column(db.String(10), nullable=False)
    floor = db.Column(db.String(10), nullable=False)
    room = db.Column(db.Integer, nullable=False)
    hall = db.Column(db.Integer, nullable=False)
    elevator = db.Column(db.String(10), nullable=False)
    bui_category = db.Column(db.String(10), nullable=False)
    property = db.Column(db.String(10), nullable=False)
    school = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        district = kwargs.pop('district')
        furnish = kwargs.pop('furnish')
        facing = kwargs.pop('facing')
        floor = kwargs.pop('floor')
        room = kwargs.pop('room')
        hall = kwargs.pop('hall')
        elevator = kwargs.pop('elevator')
        bui_category = kwargs.pop('bui_category')
        property = kwargs.pop('property')
        school = kwargs.pop('school')
        year = kwargs.pop('year')
        area = kwargs.pop('area')
        self.district = district
        self.furnish = furnish
        self.facing = facing
        self.floor = floor
        self.room = room
        self.hall = hall
        self.elevator = elevator
        self.bui_category = bui_category
        self.property = property
        self.school = school
        self.year = year
        self.area = area