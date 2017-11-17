from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#Import CRUD operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Create session and connect to DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			#Objective 5 -- Delete a restaurant
			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					message = ""
					message += "<html><body>"
					message += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
					message += "</h1>"
					message += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
					message += "<input type = 'submit' value = 'Delete'>"
					message += "</form>"
					message += "</body></html>"
					self.wfile.write(message)
					
			#Objective 4 -- Rename a restaurant
			if self.path.endswith("/edit"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					message = ""
					message += "<html><body>"
					message += "<h1>"
					message += myRestaurantQuery.name
					message += "</h1>"
					message += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%s/edit'>" % restaurantIDPath
					message += "<input name = 'newRestaurantName' type = 'text' placeholder = '%s'>" % myRestaurantQuery.name
					message += "<input type = 'submit' value = 'Rename'>"
					message += "</form>"
					message += "</body></html>"
					self.wfile.write(message)
					
			#Objective 3 Step 1 - Create /restaurants/new page
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>"
				message += "<h1>Make a New Restaurant</h1>"
				message += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'> "
				message += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
				message += "<input type = 'submit' value = 'Create'>"
				message += "</form></body></html>"
				self.wfile.write(message)
				return

			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>"
				message += "<a href = '/restaurants/new'>Make a New Restaurant Here</a>"
				message += "</br></br>"
				for restaurant in restaurants:
					message += restaurant.name
					message += "</br>"
					#Objective 2 -- Add Edit and Delete links
					#Objective 4 -- Replace Edit href
					message += "<a href = '/restaurants/%s/edit'>Edit</a>" % restaurant.id
					message += "</br>"
					#Objective 5 -- Replace Delete href
					message += "<a href = '/restaurants/%s/delete'>Delete</a>" % restaurant.id
					message += "</br></br></br>"
				message += "</body></html>"
				self.wfile.write(message)
				print message
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message = "<html><body>&#161Hola!<a href = '/hello'>Back to Hello</a></body></html>"
				message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				message += "</body></html>"
				self.wfile.write(message)
				print message
				return			

			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<hmtl><body>Hello!</body></html>"
				message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
				message += "</body></html>"
				self.wfile.write(message)
				print message
				return

		except IOError:
			self.send_error(404, 'File Not Found; %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/delete"):
				restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery:
					session.delete(myRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
				messageContent = fields.get('newRestaurantName')
				restaurantIDPath = self.path.split("/")[2]

				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery != []:
					myRestaurantQuery.name = messageContent[0]
					session.add(myRestaurantQuery)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
				messageContent = fields.get('newRestaurantName')

				#Create new Restaurant class
				newRestaurant = Restaurant (name = messageContent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()


			'''	
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			
			ctype, pdict = cgi.parse_header(
				self.headers.getheader('content-type'))
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				messageContent = fields.get('message')

			message = ""
			message += "<html><body>"
			message += "<h2> Okay, how about this: </h2>"
			message += "<h1> %s </h1>" % messageContent[0]
			
			message += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
			message += "</body></html>"
			self.wfile.write(message)
			print message
			'''
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		#print "Web Server running on port %s" % port
		print 'Web server running...open localhost:8080/restaurants in your browser'
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()

