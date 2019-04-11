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
	print(type(mm.showBible()))
	for bin in mm.showBible():
		bible.append(dict(book=bin[0], chapter=bin[1], verse_no=bin[2], verse=bin[3], id=bin[4]))
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

@app.route('/deleteVerse/<int:no>', methods=['GET', 'POST'])
@admin_access
def delete(no):
	if request.method == 'GET':
		try:
			mm.deleteVerse(no)
			print(no)
			flash('Verse Deleted')
		except Exception as e:
			flash(e)

	return redirect(url_for('home'))

	
@app.route('/searchWord', methods=['GET', 'POST'])
def search_word():
	bible = []
	error = None
	phrase = None
	if request.method == 'POST':
		returned = mm.searchWord(request.form['word'])
		if len(returned) == 0:
			error = "Word %s not found " % request.form['word']
		else:
			#phrase = returned
			try:
				for bin in returned:
					bible.append(dict(book=bin[0][0], chapter=bin[0][1], verse_no=bin[0][2], verse=bin[0][3], id=bin[0][4]))	
			except:
				pass
	return render_template('bible.html', bible=bible, title='Bible | Maranatha', error=error)
	


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
		if request.form['username'] != 'admin' or request.form['password'] != 'default':
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



