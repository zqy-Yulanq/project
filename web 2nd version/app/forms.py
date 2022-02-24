from wtforms import Form, StringField
from wtforms.validators import DataRequired, Email, Length, InputRequired, Regexp, EqualTo


# create login form
class LoginForm(Form):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='Please enter the phone number in the '
                                                                          'correct format！')])
    password = StringField(validators=[Length(3, 20, message='Please enter the password in the correct format')])


# create record form
class RecordForm(Form):
    score = StringField('score', validators=[DataRequired()])
    view_time = StringField('view_time', validators=[DataRequired()])
    content = StringField('content', validators=[DataRequired()])


