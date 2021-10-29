import DB, requests, os, liqpay3
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Response(BaseHTTPRequestHandler):
    _DB = None
    api_key = os.getenv("api_key")
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        id = post_data['id']
        apikey = post_data['api_key']
        print(post_data)
        print(self.api_key)
        print(id)
        print(apikey)
        if apikey == self.api_key:
            if(self._DB == None):
                self._DB = DB.DataBase()
            self.send_response(200)
            self.end_headers()
            data = self._DB.GetData(int(id))
            ResponseData = data[0]+";"+data[1]+";"+str(data[2])+";"+str(data[3])+";"+str(data[4])
            self.wfile.write(bytes(ResponseData, 'utf-16'))

#httpd = HTTPServer(('localhost', 8000), Response)
server_address = ('', int(os.environ.get('PORT', '3306')))
httpd = ThreadHTTPServer(server_address, Response)
httpd.serve_forever()