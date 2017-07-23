from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# lets the program know which database we want to query
Base.metadata.bind = engine
# binds the engine to the Base class -
# this makes the connections between our class definitions
# and the corresponding tables in the database
DBSession = sessionmaker(bind = engine)
# creates a sessionmaker object, which establishes a link of
# communication between our code executions and the engine we created
session = DBSession()
# create an instance of the DBSession  object - to make a changes
# to the database, we can call a method within the session

class webserverHandler(BaseHTTPRequestHandler): # extends BaseHTTPRequestHandler class
    def do_GET(self):  # handles all GET requests the web server receives - overrides the method
        try:           # in the BaseHTTPRequestHandler superclass ??
            if self.path.endswith("/restaurants"): # pattern matching that looks for end of URL
                self.send_response(200)  # send response indicating successful GET request
                self.send_header('Content-type', 'text/html') # replying with HTML format
                self.end_headers() # sends a blank line indicating the end of HTTP headers

                output = ""  # include some content to send back to the client
                output += "<html><body>"
                output += "<h1>Testing Web Server - if you can read this it's working!</h1>"
                output += "<ul>"
                names = []
                restaurantNames = session.query(Restaurant.name).order_by(Restaurant.name)
                for restaurantName in restaurantNames:
                    output += (
                        "<li> {}  -<a href='#' style='text-decoration:none'> [Edit]  <a>"
                        "<a href='#' style='text-decoration:none'> [Delete]<a></li>"
                        .format(restaurantName[0])
                        )
                output += "<ul>"

                output += "</body></html>"

                self.wfile.write(output) # function sends message back to client
                print (output) # see the output string in the terminal for debugging
                return  # exit the if statement


        except IOError:
            self.send.error(404, "File not found %s" % self.path) # Notify of error

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            print "hello!"
            # parse_header function parses an HTML form header, such as 'content-type'
            # into a main value, and a dictionary of parameters
            # uses parse_multipart to collect all the fields in the form
            # check if form data is being recieved
            # make variable to get out the value of a specific field or set of
            # fields and store them in an array

            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<h1>Process over Product - Lasting Habits Change lives!</h1>"
            # return the first value of the array that was created via form submission
            output += (
                "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>"
                "What would you like me to say?</h2><input name='message' type='text'><input"
                " type='submit' value='Submit'></form>")
            # write input field as 'message' to coincide with the message field in the POST
            output += "</body></html>"
            self.wfile.write(output) # function sends message back to client
            print (output) # see the output string in the terminal for debugging

        except:
            pass


def main():    # entry point of the code
    try:
        port = 8080 #  port defined in a separate variable
        server = HTTPServer(('',port), webserverHandler) # create instance of HTTPServer class
        # first parameter is server_address, a tuple that contains host and port number
        # second parameter is RequestHandlerClass - webserverHandler is a made up name
        print ("Web server is running on port %s") % port # good for debugging
        server.serve_forever()  # function built in to HTTPServer


    except KeyboardInterrupt:   # if a defined event occurs, we can exit with an exception
        print (" Ctrl-C entered, stopping web server...")  # more print for debugging
        server.socket.close()  #



if __name__ == '__main__':  # immediatly run main method when the Python
        main()                  # interpreter executes the script webserver.py

