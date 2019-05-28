#-*- coding: UTF-8 -*-
from app import app, db	
from app.forms import LoginForm, ActIssue, ActReceiving, ClientForm, FilmForm, IssueForm
from app.controllers import UserDomain, ClientDomain, FilmDomain, IssueDomain
from app.models import User, Client, Film, Issue
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		if UserDomain().auth(form):
			return redirect(request.args.get('next') or url_for('index'))
		else: return redirect(url_for('login'))
	return render_template('login.html', title='Вход', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/clients')
@login_required
def clients():
	clients = Client().find_all()
	return render_template('clients.html', clients=clients)

@app.route('/client/<id>')
@login_required
def client(id):
	client = ClientDomain(id)
	return render_template('client.html', client=client)

@app.route('/films')
@login_required
def films():
	films = Film().find_all()
	return render_template('films.html', films=films)

@app.route('/film/<id>')
@login_required
def film(id):
	film = FilmDomain(id)
	return render_template('film.html', film=film)

@app.route('/create_client', methods=['GET', 'POST'])
@login_required
def create_client():
	form = ClientForm()
	if form.validate_on_submit():
		print(1)
		if ClientDomain().save(form):
			flash('Клиент успешно добавлен!')
			return redirect(url_for('clients'))
	return render_template('create_client.html', title='Новый клиент',  form=form)

@app.route('/edit_client/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
	form = ClientForm()
	client = ClientDomain(id)
	if form.validate_on_submit():
		if client.save(form):
			flash('Данные успешно изменены!')
			return redirect(url_for('clients'))
	elif request.method == 'GET':
		form.name.data = client.data.name
		form.addr.data = client.data.addr
		form.phone.data = client.data.phone
		form.email.data = client.data.email
		form.passport.data = client.data.passport
	return render_template('create_client.html', title='Редактирование', form=form, client=client)

@app.route('/delete_client/<id>')
@login_required
def delete_client(id):
	ClientDomain(id).delete()
	return redirect(url_for('clients'))


@app.route('/create_film', methods=['GET', 'POST'])
@login_required
def create_film():
	form = FilmForm()
	print(2)
	if form.validate_on_submit():
		print(1)
		if FilmDomain().save(form):
			flash('Фильм успешно добавлен!')
			return redirect(url_for('films')) 
	return render_template('create_film.html', title='Новый фильм', form=form)

@app.route('/edit_film/<id>', methods=['GET', 'POST'])
@login_required
def edit_film(id):
	form = FilmForm()
	film = FilmDomain(id)
	if form.validate_on_submit():
		if film.save(form):
			flash('Фильм изменен.')
			return redirect(url_for('films'))
	elif request.method == 'GET':
		form.name.data = film.data.name
		form.studio.data = film.data.studio
		form.year.data = film.data.year
		form.duration.data = film.data.duration
		form.genre.data = film.data.genre
		form.nom_count.data = film.data.nom_count
	return render_template('create_film.html', title='Редактирование', form=form, film=film)

@app.route('/delete_film/<id>')
@login_required
def delete_film(id):
	FilmDomain(id).delete()
	return redirect(url_for('films'))

@app.route('/new_issue', methods = ['GET', 'POST'])
@login_required
def new_issue():
	form = ActIssue()
	form.client.choices = [(client.id, client.name) for client in Client().find_all()]
	form.film.choices = [(film.id, film.name) for film in Film().find_all()]
	if form.validate_on_submit():
		if IssueDomain().give_film(form):
			flash('Акт выдачи успешно создан!')
			return redirect(url_for('index'))
	return render_template('new_issue.html', title='Акт выдачи', form=form)

@app.route('/new_receiving', methods=['GET', 'POST'])
@login_required
def new_receiving():	
	form = ActReceiving()
	form.client.choices = [(client.id, client.name) for client in Client().find_all()]
	form.film.choices = [(film.id, film.name) for film in Film().find_all()]
	if form.validate_on_submit():
		issue = IssueDomain()
		if issue.find(form):
			return redirect(url_for('issue', id=issue.data.id))
		else: 
			flash('Не найдено соответсвующей выдачи!')
	return render_template('/new_receiving.html', form=form)

@app.route('/issue/<id>', methods=['GET', 'POST'])
@login_required
def issue(id):
	form = IssueForm()
	issue = IssueDomain(id)
	if form.validate_on_submit():
		if issue.take_film(form):
			flash('Операция прошла успешно!')	
			return redirect(url_for('index'))
	elif request.method == 'GET':
		form.weeks.data = issue.data.weeks
		form.sum.data = issue.data.sum
	return render_template('issue.html', title='Сдача кассеты',form=form, issue=issue)	
			
@app.route('/issues')
@login_required
def issues():
	issues = Issue.query.all()
	issue_list = []
	for issue in issues:
		issue_list.append(IssueDomain(issue.id))
	return render_template('issues.html', issues=issue_list)

		


 