import webapp2


application = webapp2.WSGIApplication([
    ('/user', 'user.User'),
    
], debug=True)

application.router.add(webapp2.Route(r'/user/<id:[0-9]+><:/?>', 'user.User'))
application.router.add(webapp2.Route(r'/user/<uid:[0-9]+>/specCar', 'specCar.SpecCar'))
application.router.add(webapp2.Route(r'/user/<uid:[0-9]+>/specCar/<sid:[0-9]+><:/?>', 'specCar.SpecCar'))
application.router.add(webapp2.Route(r'/user/<uid:[0-9]+>/specCar/<sid:[0-9]+>/fillUp', 'fillUp.FillUp'))
application.router.add(webapp2.Route(r'/user/<uid:[0-9]+>/specCar/<sid:[0-9]+>/fillUp/<fid:[0-9]+><:/?>', 'fillUp.FillUp'))
application.router.add(webapp2.Route(r'/carModel', 'carModel.CarModel'))
application.router.add(webapp2.Route(r'/carModel/<id:[0-9]+><:/?>', 'carModel.CarModel'))


