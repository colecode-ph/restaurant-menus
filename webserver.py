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

        # restaurant name probably needs to be defined here

        try:           # in the BaseHTTPRequestHandler superclass ??\

            restaurantRows = session.query(Restaurant.name, Restaurant.id).order_by(Restaurant.name)

            if self.path.endswith("/restaurants"): # pattern matching that looks for end of URL
                self.send_response(200)  # send response indicating successful GET request
                self.send_header('Content-type', 'text/html') # replying with HTML format
                self.end_headers() # sends a blank line indicating the end of HTTP headers

                output = ""  # include some content to send back to the client
                output += "<html><body>"
                output += "<h1>The List of Restaurants</h1>"
                output += "<h2><a href='/restaurants/new'>Make a New Restaurant</a></h2>"
                output += "<ul>"
                for restaurantRow in restaurantRows:
                    output += (
                        "<li> {}  -<a href='/restaurants/{}/edit' style='text-decoration:none'> [Edit]  <a>"
                        "<a href='/restaurants/{}/delete' style='text-decoration:none'> [Delete]<a></li>"
                        .format(restaurantRow[0], restaurantRow[1], restaurantRow[1])
                        )
                output += "<ul>"
                output += "</body></html>"
                self.wfile.write(output) # function sends message back to client
                print ("HTML rendered to client") # see the output string in the terminal for debugging
                return  # exit the if statement

            if self.path.endswith("/restaurants/new"): # pattern matching that looks for end of URL
                self.send_response(200)  # send response indicating successful GET request
                self.send_header('Content-type', 'text/html') # replying with HTML format
                self.end_headers() # sends a blank line indicating the end of HTTP headers

                output = ""  # include some content to send back to the client
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data'"
                output += "action='/restaurants/gnew'>"
                output += "<input type='text' name='newrestaurantName'>"
                output += "<button type='submit'>Create</button></form>"
                output += "</body></html>"
                self.wfile.write(output) # function sends message back to client
                print ("HTML rendered to client") # see the output string in the terminal for debugging
                return  # exit the if statement


            for restaurantRow in restaurantRows:

                if self.path.endswith("/restaurants/{}/edit".format(restaurantRow[1])): # pattern matching URL
                    self.send_response(200)  # send response indicating successful GET request
                    self.send_header('Content-type', 'text/html') # replying with HTML format
                    self.end_headers() # sends a blank line indicating the end of HTTP headers

                    output = ""  # include some content to send back to the client
                    output += "<html><body>"
                    output += "<h1>Edit Restaurant Name For:</h1>"
                    output += "<h2>{}</h2>".format(restaurantRow[0])
                    output += "<form method='POST' enctype='multipart/form-data'"
                    output += "action='/restaurants/{}/edit'>".format(restaurantRow[1])
                    output += "<input type='text' name='newrestaurantName'>"
                    output += "<button type='submit'>Rename</button></form>"
                    output += "</body></html>"
                    self.wfile.write(output) # function sends message back to client
                    print ("HTML rendered to client") # see the output string in the terminal for debugging
                    return  # exit the if statement

                if self.path.endswith("/restaurants/{}/delete".format(restaurantRow[1])): # pattern matching URL
                    self.send_response(200)  # send response indicating successful GET request
                    self.send_header('Content-type', 'text/html') # replying with HTML format
                    self.end_headers() # sends a blank line indicating the end of HTTP headers

                    output = ""  # include some content to send back to the client
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to Delete:</h1>"
                    output += "<h2>{}?</h2>".format(restaurantRow[0])
                    output += "<form method='POST' enctype='multipart/form-data'"
                    output += "action='/restaurants/{}/delete'>".format(restaurantRow[1])
                    # output += "<input type='text' name='newrestaurantName'>"
                    output += "<button type='submit'>Delete</button></form>"
                    output += "</body></html>"
                    self.wfile.write(output) # function sends message back to client
                    print ("HTML rendered to client") # see the output string in the terminal for debugging
                    return  # exit the if statement

        except IOError:
            self.send.error(404, "File not found %s" % self.path) # Notify of error

    def do_POST(self):
        try:

            if self.path.endswith("/restaurants/gnew"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newrestaurantName')
                else:
                    print ("FAIL!")

                # create a new Restaurant class (instance)
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                print "hello!"

            restaurantRows = session.query(Restaurant.name, Restaurant.id).order_by(Restaurant.name)
            for restaurantRow in restaurantRows:

                if self.path.endswith("/restaurants/{}/edit".format(restaurantRow[1])):
                # if self.path.endswith("/restaurants/edit"):
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('newrestaurantName')

                        # Update Restaurant Name
                        id = restaurantRow[1]
                        updateName = session.query(Restaurant).get(id)
                        updateName.name = messagecontent[0]
                        session.add(updateName)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print "hello!"


                if self.path.endswith("/restaurants/{}/delete".format(restaurantRow[1])):
                # if self.path.endswith("/restaurants/edit"):
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('newrestaurantName')

                        # Delete Restaurant Name
                        id = restaurantRow[1]
                        updateName = session.query(Restaurant).get(id)
                        # updateName.name = messagecontent[0]
                        session.delete(updateName)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print "hello!"
                    # parse_header function parses an HTML form header, such as 'content-type'
                    # into a main value, and a dictionary of parameters
                    # uses parse_multipart to collect all the fields in the form
                    # check if form data is being recieved
                    # make variable to get out the value of a specific field or set of
                    # fields and store them in an array
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

