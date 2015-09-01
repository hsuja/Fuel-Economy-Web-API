import webapp2
from google.appengine.ext import ndb
import db_defs
import json

class CarModel(webapp2.RequestHandler):

	def get(self, **kwargs):

		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "API only supports application/json"
			return

		p_key = ndb.Key(db_defs.CarModel, 'p_key')

		if 'id' in kwargs:
			out = ndb.Key(db_defs.CarModel, int(kwargs['id']), parent = p_key).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_defs.CarModel.query(ancestor = p_key)
			keys = q.fetch(keys_only = True)

			results = {'carModels':[x.get().to_dict() for x in keys]}
			self.response.write(json.dumps(results))
