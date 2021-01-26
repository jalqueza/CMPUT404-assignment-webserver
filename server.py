#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request = self.data.decode('utf-8').split()
        method = request[0]
        url = request[1]

        if method != "GET":
            self.error_405()
        else:
            self.get_request(url)
    
    def get_request(self, url):
        
        if "../" in url:
            return self.error_404()
        
        url =  "www" + url
        if url[-1] == "/":
            url = url + "index.html"        
        
        print(url)
        if os.path.isdir(url):
            return self.error_301(url)

        elif os.path.exists(url):
            # TODO: suppourt mime-types HTML CSS?
            response = "HTTP/1.1 200 OK"
            self.request.sendall(response.encode('utf-8'))

            file_to_open = open(url).read()
            self.request.sendall(file_to_open.encode('utf-8'))

        else:
            print("HERE1")
            return self.error_404()


    def error_405(self):
        response = "HTTP/1.1 405 Method Not Allowed"
        self.request.sendall(response.encode('utf-8'))

    def error_404(self):
        response = "HTTP/1.1 404 Not Found"
        self.request.sendall(response.encode('utf-8'))
    
    def error_301(self, url):
        print(url)
        response = f'HTTP/1.1 301 Moved Permanently \r\n{url}/'
        self.request.sendall(response.encode('utf-8'))
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
