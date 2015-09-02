import webapp2
from google.appengine.ext import ndb
import db_defs
import json

class SpecCar(webapp2.RequestHandler):

	def post(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		if 'uid' in kwargs:
			user_key = ndb.Key(db_defs.User, int(kwargs['uid']))
			new_specCar = db_defs.SpecCar(parent = user_key)
		else: 
			new_specCar = db_defs.SpecCar()

		year = self.request.get('year', default_value = None)
		make = self.request.get('make', default_value = None)
		model = self.request.get('model', default_value = None)
		fuelecon = self.request.get('fuelecon', default_value = None)
		fillups = self.request.get_all('fillups[]', default_value = None)

		if year: 
			new_specCar.year = year
		else:
			self.response.status = 400
			self.response.status_message = "Model year required"
			return

		if make: 
			new_specCar.make = make
		else:
			self.response.status = 400
			self.response.status_message = "Make required"
			return

		if model: 
			new_specCar.model = model
		else:
			self.response.status = 400
			self.response.status_message = "Model required"
			return
		
		if fuelecon:
			new_specCar.fuelecon = fuelecon

		if fillups:
			for fillup in fillups:
				new_specCar.fillups.append(ndb.Key(db_defs.Car, int(fillup)))
		key = new_specCar.put()


		if 'uid' in kwargs:
			user = user_key.get()
			user.cars.append(new_specCar.key)
			user.put()

		#add car to CarModel 			
		p_key = ndb.Key(db_defs.CarModel, 'p_key')
		q = db_defs.CarModel.query(ancestor = p_key)
		q = q.filter(db_defs.CarModel.year == year)
		q = q.filter(db_defs.CarModel.make == make)
		q = q.filter(db_defs.CarModel.model == model)
		
		if q.count(limit=None) == 0:
			new_carModel = db_defs.CarModel(parent = p_key)
			new_carModel.year = year
			new_carModel.make = make
			new_carModel.model = model
			new_carModel.distance = 0
			new_carModel.fuelused = 0
			new_carModel.put()
		else:
			self.response.write("car model already in CarModel!")


		out = new_specCar.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		if 'uid' in kwargs:

			if 'sid' in kwargs:
				user_key = ndb.Key(db_defs.User, int(kwargs['uid'])) 
				out = ndb.Key(db_defs.SpecCar, int(kwargs['sid']), parent = user_key).get().to_dict()
				self.response.write(json.dumps(out))
			else:
				user_key = ndb.Key(db_defs.User, int(kwargs['uid'])) 
				q = db_defs.SpecCar.query(ancestor = user_key)
				keys = q.fetch(keys_only = True)

				results = {'specCars':[x.get().to_dict() for x in keys]}
				self.response.write(json.dumps(results))

		else: 
			self.response.status = 400
			self.response.status_message = "User ID required"
			return


	




