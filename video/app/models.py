from datetime import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	name = db.Column(db.String(150))
	password = db.Column(db.String(50))
	email = db.Column(db.String(120), unique=True)
	
	def __repr__(self):
		return '<User {}>'.format(self.username)

	def check_password(self, password):
		return self.password == password
		
	def find_by_username(username):
		return User.query.filter_by(username=username).first()
	
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), index=True)
	addr = db.Column(db.String(250))
	phone = db.Column(db.String(10))
	email = db.Column(db.String(50))
	passport = db.Column(db.String(10))
	
	def __repr__(self):
		return '<Client {}}>'.format(self.name)

	def insert(self, name, addr, phone, email, passport):
		self.name = name
		self.addr = addr	
		self.phone = phone	
		self.email = email
		self.passport = passport
		db.session.add(self)
		db.session.commit()
		
	def update(self, name,addr, phone, email, passport):
		self.name = name
		self.addr = addr
		self.phone = phone	
		self.email = email
		self.passport = passport
		db.session.commit()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()
		
	def find_all(self):
		return Client.query.all()
	
	def find(self,id):
		return Client.query.filter_by(id=id).first()
		
		
class Film(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True)
	studio = db.Column(db.String(100))
	year = db.Column(db.String(4))
	duration = db.Column(db.Integer)
	genre = db.Column(db.String(50))
	nom_count = db.Column(db.Integer)
	fact_count = db.Column(db.Integer)

	def __repr__(self):
		return '<Film {}>'.format(self.name)

	def insert(self, name, studio, year, duration, genre, nom_count, fact_count):
		self.name = name
		self.studio = studio	
		self.year = year	
		self.duration = duration
		self.genre = genre
		self.nom_count = nom_count
		self.fact_count = fact_count
		db.session.add(self)
		db.session.commit()
		
	def update(self, name, studio, year, duration, genre, nom_count, fact_count):
		self.name = name
		self.studio = studio	
		self.year = year	
		self.duration = duration
		self.genre = genre
		self.nom_count = nom_count
		self.fact_count = fact_count
		db.session.commit()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def decrease(self):
		self.fact_count -= 1
		db.session.commit()
		
	def increase(self):
		self.fact_count += 1
		db.session.commit()
		
	def find_all(self):
		return Film.query.all()
	
	def find(self, id):
		return Film.query.filter_by(id=id).first()	

class Issue(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'), index=True)
	film_id = db.Column(db.Integer, db.ForeignKey('film.id'), index=True)
	date = db.Column(db.DateTime)
	weeks = db.Column(db.Integer)
	sum = db.Column(db.Float)

	def __repr__(self):
		return '<Issuance {}>'.format(self.id)
		
	def find_film_by_client(self, client_id):
		return self.query(film_id).filter_by(client_id=client_id)
		
	def find(self, client_id, film_id):
		return self.query.filter_by(client_id=client_id, film_id=film_id).first()
		
	def find_by_id(self, id):
		return self.query.filter_by(id=id).first()		

	def insert(self, client_id, film_id, date, weeks, sum):
		self.client_id = client_id
		self.film_id = film_id	
		self.date = date	
		self.weeks = weeks
		self.sum = sum
		db.session.add(self)
		db.session.commit()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()