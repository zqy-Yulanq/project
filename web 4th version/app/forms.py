from wtforms import Form, StringField
from wtforms.validators import Length,  Regexp


# Create login form
class LoginForm(Form):
    telephone = StringField(validators=[Regexp(r"1[345789]\d{9}", message='Please enter the phone number in the '
                                                                          'correct format！')])
    password = StringField(validators=[Length(3, 20, message='Please enter the password in the correct format')])


