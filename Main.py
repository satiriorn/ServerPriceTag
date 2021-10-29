import DB, requests, os, liqpay3
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Response(BaseHTTPRequestHandler):
    _DB = None

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print(post_data)
        if(self._DB == None):
            self._DB = DB.DataBase()
        self.send_response(200)
        self.end_headers()
        data = self._DB.GetData(int(post_data))
        ResponseData = data[0]+";"+data[1]+";"+str(data[2])+";"+str(data[3])+";"+str(data[4])
        self.wfile.write(bytes(ResponseData, 'utf-16'))

#httpd = HTTPServer(('localhost', 8000), Response)
server_address = ('', int(os.environ.get('PORT', '3306')))
httpd = ThreadHTTPServer(server_address, Response)
httpd.serve_forever()