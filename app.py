#!/usr/bin/python3

from flask import (Flask, request, flash, redirect, render_template,
session, url_for)
from functools import wraps
import sqlite3
import models.models as mm

app = Flask(__name__)

app.secret_key = b'What-cat-be-kept-here-*******//********\\**'

def admin_access(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
    	if 'logged_in' in session:
    		return f(*args, **kwargs)
    	else:
    		flash("You need to login First.")
    		return redirect(url_for('login'))
    return wrapper_function

@app.route('/')
def home():
	bible = []
	for bin in mm.showBible():
		bible.append(dict(book=bin[0], chapter=bin[1], verse_no=bin[2], verse=bin[3]))
	#print(bible)
	return render_template('bible.html', bible=bible, title='Bible | Maranatha')



@app.route('/addverse', methods=['GET', 'POST'])
@admin_access
def add_verse():
	if request.method == 'POST':	

		try:
			mm.addVerse(request.form['book'], request.form['chapter'], request.form['verse_no'], request.form['verse'])
			flash('Added successfully')
		except sqlite3.IntegrityError as e:
			flash('Duplicate verses adding is not allowed.', e.args[0])


	return render_template('addverse.html')	

@app.route('/deleteVerse', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		try:
			mm.deleteVerse(request.form[id])
			flash('Verse Deleted')
		except Exception as e:
			flash(e)

	return render_template('index.html')

	
@app.route('/editverse', methods=['GET', 'POST'])
@admin_access
def edit_verse():
	try:
		mm.updateRow(request.form['verse'], request.form['id'])
		flash('Updated successfully!!')
	except Exception as e:
		pass
	return redirect(url_for('home'))
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' and request.form['password'] != 'default':
			error = ( "Invalid login details. Try again")
		else:
			session['logged_in']=True
			flash('You are logged in')
			return redirect(url_for('add_verse'))
	return render_template('login.html', error=error)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=1122, debug=True)



