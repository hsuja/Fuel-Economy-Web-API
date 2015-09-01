import webapp2
from google.appengine.ext import ndb
import db_defs
import json

class User(webapp2.RequestHandler):

	def post(self):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		new_user = db_defs.User()
		username = self.request.get('username', default_value = None)
		name = self.request.get('name', default_value = None)
		password = self.request.get('password', default_value = None)
		email = self.request.get('email', default_value = None)
		cars = self.request.get_all('cars[]', default_value = None)

		if username: 
			new_user.username = username
		else:
			self.response.status = 400
			self.response.status_message = "Username required"
			return
		if name:
			new_user.name = name
		if password:
			new_user.password = password
		if email:
			new_user.email = email
		if cars:
			for car in cars:
				new_user.cars.append(ndb.Key(db_defs.Car, int(car)))
		key = new_user.put()
		out = new_user.to_dict()
		self.response.write(json.dumps(out))

		return

	def get(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		if 'id' in kwargs:
			#test = ndb.Key(db_defs.User, int(kwargs['id'])).get()
			#self.response.write(test)
			out = ndb.Key(db_defs.User, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else: 
			q = db_defs.User.query()
			keys = q.fetch(keys_only = True)
			
			results = {'users':[x.get().to_dict() for x in keys]}
			self.response.write(json.dumps(results))


			#for x in keys:
			#	self.response.write(json.dumps(x.get().to_dict()))



	def put(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		new_username = self.request.get('newUsername', default_value = None)	
		new_name = self.request.get('newName', default_value = None)
		new_pass = self.request.get('newPass', default_value = None)	
		new_email = self.request.get('newEmail', default_value = None)		

		if 'id' in kwargs:
			user_key = ndb.Key(db_defs.User, int(kwargs['id']))
			user = user_key.get()

			if new_username:
				user.username = new_username
			if new_name:
				user.name = new_name
			if new_pass:
				user.password = new_pass
			if new_email:
				user.email = new_email

			user.put()
			out = user.to_dict()
			self.response.write(json.dumps(out))
			return

