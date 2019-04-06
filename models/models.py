import sqlite3


def createDb():
	database = sqlite3.connect('bibledb.db')

	return database

def createTable():
	con = createDb()
	cur = con.cursor()
	cur.execute('''
				CREATE TABLE IF NOT EXISTS bibleTable(
				book VARCHAR(30) NOT NULL,
				chapter int NOT NULL,
				verse_no int NOT NULL, 
				verse text NOT NULL,
				id INTEGER PRIMARY KEY AUTOINCREMENT ,
				CONSTRAINT verse_info UNIQUE (book, chapter, verse_no )) 
			''') 
	
	
def updateRow(mstari, hiyo):
	con = createDb()
	cur =	con.execute('UPDATE bibleTable set verse=("%s") WHERE id=(%d)' %(mstari, int(hiyo)))
	print(cur.fetchall())
	con.commit()

def dropTable():
	con = createDb()
	con.execute('DROP TABLE IF EXISTS bibleTable')
	con.commit()
	# con.close()

def addVerse(book, chapter, verse_no, verse):
	con = createDb()
	# c = con.cursor()
	con.execute('INSERT INTO bibleTable (book, chapter, verse_no, verse) VALUES(?, ?, ?, ?)',  (book, chapter, verse_no, verse))
	con.commit()
	# con.close()
def deleteVerse(id):
	con = createDb()
	con.execute('DELETE FROM bibleTable where id=(%d)' % (id))
	con.commit()

def show_book_chapter(book, chapter):
	con = createDb()
	returnlist = list()
	cur = con.cursor()
	cur.execute(('SELECT * FROM bibleTable WHERE book=("%s") and chapter=("%s")' %(book, chapter)))
	ver = list(cur.fetchall())
	no_of_chapters = con.execute(('SELECT COUNT(verse) from bibleTable WHERE book=("%s") and chapter=("%s")' %(book, chapter)))	
	no = list(no_of_chapters.fetchone())
	no_of = int(no[0])

	for i in range(no_of):
		returnlist.append(ver[i][0])
		returnlist.append(ver[i][1])
		returnlist.append(ver[i][2])
		returnlist.append( ver[i][3])

	con.commit()
	con.close()	

	return returnlist

def searchWord(word):
	con = createDb()
	cur = con.cursor()
	cur.execute('SELECT * FROM bibleTable ')
	resp = list(cur.fetchall())
	foundverses = list()
	res = list()
	for i in resp:
		res.append(i[3])


	for re in res:
		if word in re:
			cur.execute('select * FROM bibleTable WHERE verse=("%s")' % re)
			foundverses.append(list(cur.fetchall()))

	return foundverses

def showBible():
	con = createDb()
	cur = con.execute('SELECT * from bibleTable ORDER BY verse_no asc')

	new = list(cur.fetchall())

	return new