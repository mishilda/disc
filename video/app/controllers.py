from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from app.models import User, Client, Film, Issue
from werkzeug.urls import url_parse
from datetime import datetime

class UserDomain():
	def __init__(self, id=None):
		if id is not None:
			self.data = User().find(id)
		
	def auth(self, form):
		user = User.find_by_username(form.username.data)
		if user is not None and user.check_password(form.password.data):
			self.data = user
			login_user(user, form.remember_me.data)
			return True
		flash('Неверный логин или пароль!')
		return False

class ClientDomain():
	def __init__(self, id=None):
		if id is not None:
			self.data = Client().find(id)
			self.new = False
		else:	self.new = True

	def find_films(self):    	
		self.films = []
		films_id = Issue().find_film_by_client(self.data.id)
		for film_id in films_id:
			self.films.append(FilmDomain().find(film_id))
			
		
	def save(self, form):
		name = form.name.data
		addr = form.addr.data
		phone = form.phone.data
		email = form.email.data
		passport = form.passport.data
		if self.new:
			Client().insert(name, addr, phone, email, passport)
		else:	self.data.update(name, addr, phone, email, passport)
		return True

	def delete(self):       
		self.data.delete()
		

class FilmDomain():
	def __init__(self, id=None):
		if id is not None:
			self.data = Film().find(id)
			self.new = False
		else:	self.new = True

	def find(self, film_id):
		return Film().find(film_id)
		
		
	def save(self, form):
		name = form.name.data
		studio = form.studio.data
		year = form.year.data
		duration = form.duration.data
		genre = form.genre.data
		nom_count = form.nom_count.data
		if self.new:
			Film().insert(name, studio, year, duration, genre, nom_count, fact_count=nom_count)
		else:	self.data.update(name, studio, year, duration, genre, nom_count, fact_count=self.data.fact_count)
		return True
		
	def delete(self):       
		self.data.delete()

class IssueDomain():
	def __init__(self, id=None):
		if id is not None:
			self.data = Issue().find_by_id(id)
			self.client = ClientDomain(self.data.client_id)
			self.film = FilmDomain(self.data.film_id)
			self.new = False
		else:	self.new = True
	
	def find(self, form):
		self.data = Issue().find(form.client.data, form.film.data)
		if self.data == None:
			return False
		else: return True
	
	def give_film(self, form):
		client_id = form.client.data
		film_id = form.film.data
		weeks = form.weeks.data
		sum = form.sum.data
		date = datetime.utcnow()
		film = FilmDomain(film_id)
		if film.data.fact_count > 0:
			Issue().insert(client_id, film_id, date, weeks, sum)
			film.data.decrease()
			return True
		flash('Нет кассет в наличии!')
		return False
		
	def take_film(self, form):      
		self.film.data.increase()
		self.data.delete()
		return True