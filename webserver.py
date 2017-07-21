from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler): # extends BaseHTTPRequestHandler class
    def do_GET(self):  # handles all GET requests the web server receives
        try:
            if self.path.endswith("/hello"): # pattern matching that looks for end of URL
                self.send_response(200)  # send response indicating successful GET request
                self.send_header('Content-type', 'text/html') # replying with HTML format
                self.end_headers() # sends a blank line indicating the end of HTTP headers

                output = ""  # include some content to send back to the client
                output += "<html><body><h1>Hello!</h1></body></html>" # add HTML to output stream
                self.wfile.write(output) # function sends message back to client
                print (output) # see the output string in the terminal for debugging
                return  # exit the if statement

        except IOError:
            self.send.error(404, "File not found %s" % self.path) # Notify of error

def main():    # entry point of the code
    try:
        port = 8080 #  port defined in a separate variable
        server = HTTPServer(('',port), webserverHandler) # create instance of HTTPServer class
        # first parameter is server_address, a tuple that contains host and port number
        # second parameter is RequestHandlerClass - webserverHandler is a made up name
        print ("Web server is running on port %s") % port # good for debugging
        server.serve_forever()  # function built in to HTTPServer


    except KeyboardInterrupt:   # if a defined event occurs, we can exit with an exception
        print ("Ctrl-C entered, stopping web server...")  # more print for debugging
        server.socket.close()  #



if __name__ == '__main__':  # immediatly run main method when the Python
        main()                  # interpreter executes the script webserver.py