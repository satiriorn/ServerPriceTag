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
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        data = post_data.decode('utf-8')
        x = data.split("&")
        apikey = x[0].split("=")[1]
        id = x[1].split("=")[1]
        if apikey == self.api_key:
            if(self._DB == None):
                self._DB = DB.DataBase()
            self.send_response(200)
            self.end_headers()
            data = self._DB.GetData(int(id))
            ResponseData = "<tr> <td>"+data[0]+"#"+data[1]+"#"+str(data[2])+"#"+str(data[3])+"#"+str(data[4])+"</td> </tr>"
            self.wfile.write(ResponseData.encode('utf-8'))

#httpd = HTTPServer(('localhost', 8000), Response)
httpd = ThreadHTTPServer(('', int(os.environ.get('PORT', '3306'))), Response)
httpd.serve_forever()