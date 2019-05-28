from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateField, IntegerField  
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user

class LoginForm(FlaskForm):
	username = StringField('Логин', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить меня')
	submit = SubmitField('Войти')
	
	
class ClientForm(FlaskForm):
	name = StringField('ФИО', validators=[DataRequired()])
	addr = StringField('Адрес', validators=[DataRequired()])
	phone = StringField('Телефон', validators=[DataRequired(), Length(min=0, max=10)])
	email = StringField('e-mail', validators=[DataRequired()])
	passport = StringField('Номер паспорта', validators=[DataRequired(), Length(min=0, max=10)])
	submit = SubmitField('Сохранить')

class FilmForm(FlaskForm):
	name = StringField('Название', validators=[DataRequired()])
	studio = StringField('Студия', validators=[DataRequired()])
	year = StringField('Год', validators=[DataRequired(), Length(min=0, max=4)])
	duration = IntegerField('Длительность в минутах', validators=[DataRequired()])
	genre = StringField('Жанр', validators=[DataRequired()])
	nom_count = IntegerField('Количество кассет', validators=[DataRequired()])
	submit = SubmitField('Сохранить')

class ActIssue(FlaskForm):
	client = SelectField('Клиент', coerce=int,  validators=[DataRequired()])
	film = SelectField('Фильм', coerce=int,  validators=[DataRequired()])
	weeks = IntegerField('Количество недель проката',  validators=[DataRequired()])
	sum = StringField('Стоимость проката',  validators=[DataRequired()])
	submit = SubmitField('Сохранить')
	
class ActReceiving(FlaskForm):
	client = SelectField('Клиент', coerce=int,  validators=[DataRequired()])
	film = SelectField('Фильм', coerce=int,  validators=[DataRequired()])
	submit = SubmitField('Найти')

class IssueForm(FlaskForm):
	weeks = IntegerField('Количество недель проката',  validators=[DataRequired()])
	sum = StringField('Стоимость проката',  validators=[DataRequired()])
	submit = SubmitField('Принять')