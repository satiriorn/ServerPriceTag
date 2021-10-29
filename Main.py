import DB, requests, os
from liqpay3 import LiqPay
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass
"""
liqpay = LiqPay()
html = liqpay.cnb_form({
    'action': 'pay',
    'amount': '1',
    'currency': 'USD',
    'description': 'description text',
    'order_id': 'order_id_1',
    'version': '3'
})
print(liqpay)
print(html)
"""
class Response(BaseHTTPRequestHandler):
    _DB = None
    def do_GET(self):
        if(self._DB == None):
            self._DB = DB.DataBase()
        self.send_response(200)
        self.end_headers()
        data = self._DB.GetData(1)
        print(data)
        print(data[0])
        ResponseData = data[0]+";"+data[1]+";"+str(data[2])+";"+str(data[3])+";"+str(data[4])
        self.wfile.write(bytes(ResponseData, 'utf-16'))
        #self.path = '/index.html'
        #file_to_open = open(self.path[1:]).read()
        #self.wfile.write(bytes(file_to_open, 'utf-8'))
        #self.end_headers()

#httpd = HTTPServer(('localhost', 8000), Response)
server_address = ('', int(os.environ.get('PORT', '3306')))
httpd = ThreadHTTPServer(server_address, Response)
httpd.serve_forever()