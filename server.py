#  coding: utf-8
import socketserver

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
        print("Got a request of: %s\n" % self.data)
        req = self.data.decode().split()
        print(req)
        if req[0] == "GET":
            if req[1][-1:] == "/":
                content = open("./www"+req[1]+"index.html",'r').read()
                self.request.send("HTTP/1.1 200 OK \r\n".encode())
                self.request.send("Content-Type: text/html; \r\n\r\n".encode())
                self.request.send(content.encode())
            else:  
                try:
                    if req[1][-4:]==".css":
                        content = open("./www"+req[1],'r').read()
                        self.request.send("HTTP/1.1 200 OK \r\n".encode())
                        self.request.send("Content-Type: text/css \r\n\r\n".encode())
                        self.request.send(content.encode())
                            
                    elif req[1][-5:]==".html":
                        content = open("./www"+req[1],'r').read()
                        self.request.send("HTTP/1.1 200 OK\r\n".encode())
                        self.request.send("Content-Type: text/html \r\n\r\n".encode())
                        self.request.send(content.encode())
                    else:
                        content = open("./www"+req[1]+"/index.html",'r').read()
                        self.request.send("HTTP/1.1 301 Moved Permanently\r\n".encode())
                        location="Location: 127.0.0.1:8080"+req[1]+"/ \r\n"
                        self.request.send(location.encode())
                except:
                    self.request.send("HTTP/1.1 404 Not Found \r\n".encode())
        else:
            self.request.send("HTTP/1.1 405 \r\n".encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
