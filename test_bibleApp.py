import unittest
from app import app

class TestingBibleApp(unittest.TestCase):

	'''Test if it runs / loads correctly '''
	def test_index(self):
		tester = app.test_client(self)
		resp = tester.get('/', content_type='html/text')
		self.assertTrue(resp.status_code, 200)

	'''Test contents oads from database'''
	def test_data_loads_from_database(self):
		tester = app.test_client(self)
		resp = tester.get('/', content_type='html/text')
		self.assertTrue(b'In the beginning was the Word,' in resp.data)

	'''Test the user must be logged in to add a new verse'''
	def test_need_login_to_add_verse(self):
		tester = app.test_client(self)
		resp = tester.get('/addverse', content_type='html/text')
		self.assertTrue(b'You need to login First.', resp.data)


	'''test for correct/incorrect '''
	def test_incorrect_logins(self):
		tester = app.test_client(self)
		resp = tester.post('/login', data=dict(username='new', password='old'), follow_redirects=True)
		self.assertIn(b'Invalid login details. Try again', resp.data)


	'''test correct logins'''
	def test_correct_logins(self):
		tester = app.test_client(self)
		resp = tester.post('/login', data=dict(username='admin', password='default'), follow_redirects=True)
		self.assertIn(b'You are logged in', resp.data)

if __name__ == '__main__':
	unittest.main()
