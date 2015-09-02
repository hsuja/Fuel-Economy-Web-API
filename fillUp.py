import webapp2
from google.appengine.ext import ndb
import db_defs
import json
from datetime import datetime

class FillUp(webapp2.RequestHandler):

	def post(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		if 'sid' in kwargs:
			user_key = ndb.Key(db_defs.User, int(kwargs['uid']))
			specCar_key = ndb.Key(db_defs.SpecCar, int(kwargs['sid']), parent = user_key)
			new_fillUp = db_defs.FillUp(parent = specCar_key)
		else: 
			new_fillUp = db_defs.FillUp()


		date = self.request.get('date', default_value = None)
		distance = float(self.request.get('distance', default_value = None))
		fuelused = float(self.request.get('fuelused', default_value = None))
		latitude = self.request.get('latitude', default_value = None)
		longitude = self.request.get('longitude', default_value = None)

		if date:
			new_fillUp.date = (datetime.strptime(date, '%m-%d-%Y')).date()

		if distance: 
			new_fillUp.distance = distance
		else:
			self.response.status = 400
			self.response.status_message = "Distance required"
			return

		if fuelused: 
			new_fillUp.fuelused = fuelused
		else:
			self.response.status = 400
			self.response.status_message = "Fuel used required"
			return

		if latitude:
			new_fillUp.latitude = latitude

		if longitude:
			new_fillUp.longitude = longitude

		fuelecon = distance/fuelused
		new_fillUp.fuelecon = fuelecon

		new_fillUp.put()

		if 'sid' in kwargs:
			specCar = specCar_key.get()
			specCar.fillups.append(new_fillUp.key)
			specCar.put()

			year = specCar.year
			make = specCar.make
			model = specCar.model

			# Update avg fuel economy of specific car
			q = db_defs.FillUp.query(ancestor = specCar_key)
			count = 0
			total_fe = 0
			for x in q:
				count = count + 1
				total_fe = total_fe + x.fuelecon
			if count > 0:
				avg_fe = total_fe/count
				specCar.fuelecon = avg_fe
				specCar.put()

		# Update CarModel
		p_key = ndb.Key(db_defs.CarModel, 'p_key')
		q = db_defs.CarModel.query(ancestor = p_key)
		q = q.filter(db_defs.CarModel.year == year)
		q = q.filter(db_defs.CarModel.make == make)
		q = q.filter(db_defs.CarModel.model == model)
		
		keys = q.fetch(keys_only = True)
		carModel_key = keys[0]
		carModel = carModel_key.get()
		
		new_distance = carModel.distance + distance
		new_fuelused = carModel.fuelused + fuelused
		new_fuelecon = new_distance/new_fuelused
		
		carModel.distance = new_distance
		carModel.fuelused = new_fuelused
		carModel.fuelecon = new_fuelecon
		carModel.put()
		
		out = new_fillUp.to_dict()
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
				specCar_key = ndb.Key(db_defs.SpecCar, int(kwargs['sid']), parent = user_key) 

				if 'fid' in kwargs:
					out = ndb.Key(db_defs.FillUp, int(kwargs['fid']), parent = specCar_key).get().to_dict()
					self.response.write(json.dumps(out))
				else:
					q = db_defs.FillUp.query(ancestor = specCar_key)
					keys = q.fetch(keys_only = True)
					results = {'fillUps':[x.get().to_dict() for x in keys]}
					self.response.write(json.dumps(results))

			else:
				self.response.status = 400
				self.response.status_message = "SpecCar ID required"
				return


		else: 
			self.response.status = 400
			self.response.status_message = "User ID required"
			return

	def delete(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		if 'uid' in kwargs:

			if 'sid' in kwargs:
				user_key = ndb.Key(db_defs.User, int(kwargs['uid']))
				specCar_key = ndb.Key(db_defs.SpecCar, int(kwargs['sid']), parent = user_key) 
				specCar = specCar_key.get()
				

				if 'fid' in kwargs:
					fillUp_key = ndb.Key(db_defs.FillUp, int(kwargs['fid']), parent = specCar_key)
					fillUp = fillUp_key.get()
					distance = fillUp.distance
					fuelused = fillUp.fuelused
					fillUp_key.delete()

					# update the specCar list of fillups and fuel economy
					specCar.fillups.remove(fillUp_key)
					specCar.put()

					q = db_defs.FillUp.query(ancestor = specCar_key)
					count = 0
					total_fe = 0
					for x in q:
						count = count + 1
						total_fe = total_fe + x.fuelecon
					if count > 0:
						avg_fe = total_fe/count
						specCar.fuelecon = avg_fe
						specCar.put()
					else:
						specCar.fuelecon = None
						specCar.put()

					#update CarModel
					year = specCar.year
					make = specCar.make
					model = specCar.model

					p_key = ndb.Key(db_defs.CarModel, 'p_key')
					q = db_defs.CarModel.query(ancestor = p_key)
					q = q.filter(db_defs.CarModel.year == year)
					q = q.filter(db_defs.CarModel.make == make)
					q = q.filter(db_defs.CarModel.model == model)

					keys = q.fetch(keys_only = True)
					carModel_key = keys[0]
					carModel = carModel_key.get()

					if count > 0:
						new_distance = carModel.distance - distance
						new_fuelused = carModel.fuelused - fuelused
						new_fuelecon = new_distance/new_fuelused
						carModel.distance = new_distance
						carModel.fuelused = new_fuelused
						carModel.fuelecon = new_fuelecon
						carModel.put()		
					else:
						carModel.distance = 0
						carModel.fuelused = 0
						carModel.fuelecon = None
						carModel.put()

				else:
					self.response.status = 400
					self.response.status_message = "FillUp ID required"
					return

			else:
				self.response.status = 400
				self.response.status_message = "SpecCar ID required"
				return


		else: 
			self.response.status = 400
			self.response.status_message = "User ID required"
			return




