from google.appengine.ext import ndb
from datetime import datetime

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class User(Model):
	username = ndb.StringProperty(required = True)
	name = ndb.StringProperty()
	password = ndb.StringProperty()
	email = ndb.StringProperty()
	cars = ndb.KeyProperty(repeated = True)

	def to_dict(self):
		d = super(User, self).to_dict()
		d['cars'] = [x.id() for x in d['cars']]
		return d

class SpecCar(Model):
	year = ndb.StringProperty(required = True)
	make = ndb.StringProperty(required = True)
	model = ndb.StringProperty(required = True)
	fuelecon = ndb.FloatProperty()
	fillups = ndb.KeyProperty(repeated = True)

	def to_dict(self):
		d = super(SpecCar, self).to_dict()
		d['fillups'] = [x.id() for x in d['fillups']]
		return d

class FillUp(Model):
	date = ndb.DateProperty()
	distance = ndb.FloatProperty(required = True)
	fuelused = ndb.FloatProperty(required = True)
	fuelecon = ndb.FloatProperty(required = True)
	latitude = ndb.StringProperty()
	longitude = ndb.StringProperty()

	def to_dict(self):
		d = super(FillUp, self).to_dict()
		if d['date']:
			d['date'] = d['date'].strftime('%m-%d-%Y')
		return d

class CarModel(Model):
	year = ndb.StringProperty(required = True)
	make = ndb.StringProperty(required = True)
	model = ndb.StringProperty(required = True)
	distance = ndb.FloatProperty(required = True)
	fuelused = ndb.FloatProperty(required = True)
	fuelecon = ndb.FloatProperty()


