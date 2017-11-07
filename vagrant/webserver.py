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
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<hmtl><body>Hello!</body></html>"
				message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>'''
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
				message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>'''
				message += "</body></html>"
				self.wfile.write(message)
				print message
				return

			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>"
				for restaurant in restaurants:
					message += restaurant.name
					message += "</br>"
				message += "</body></html>"
				self.wfile.write(message)
				print message
				return

		except IOError:
			self.send_error(404, 'File Not Found; %s' % self.path)

	def do_POST(self):
		try:
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
			
			message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>'''
			message += "</body></html>"
			self.wfile.write(message)
			print message
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()

