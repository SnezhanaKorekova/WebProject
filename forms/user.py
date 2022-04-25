from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('фамилия', validators=[DataRequired()])
    name = StringField('имя', validators=[DataRequired()])
    email = EmailField('почта', validators=[DataRequired()])
    password = PasswordField('пароль', validators=[DataRequired()])
    password_again = PasswordField('повторите пароль', validators=[DataRequired()])
    phone = StringField('телефон', validators=[DataRequired()])
    submit = SubmitField('войти')


class LoginForm(FlaskForm):
    email = EmailField('почта', validators=[DataRequired()])
    password = PasswordField('пароль', validators=[DataRequired()])
    remember_me = BooleanField('запомнить меня')
    submit = SubmitField('войти')