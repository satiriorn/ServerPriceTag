import DB, requests, os, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from liqpay3 import LiqPay

class ThreadHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class Response(BaseHTTPRequestHandler):
    _DB = None
    api_key = os.getenv("api_key")
    count = 1
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
            ResponseData = "<tr> <td>"+data[0]+"#"+data[1]+"#"+str(data[2])+"#"+str(data[3])+"#"+str(data[4])+"#"+str(data[5])+"#"\
                           + time.strftime("%H", time.localtime())+"</td> </tr>"
            self.wfile.write(ResponseData.encode('utf-8'))

    def do_GET(self):
        price_id = self.path.replace("/", "")
        if len(price_id) > 0:
            if (self._DB == None):
                self._DB = DB.DataBase()
            data = self._DB.GetData(int(price_id))
            if len(data) > 0:
                self.send_response(302)
                self.send_header('Location', self.link_pay(data))
                self.end_headers()

    @classmethod
    def link_pay(cls, data):
        liqpay = LiqPay(os.getenv("public_key"), os.getenv("private_key"))
        cls.count+=1
        if(data[4] == True): price = data[3]
        else: price = data[2]
        print(data[4])
        d = {
            'action': 'pay',
            'amount':  price,
            'currency': 'UAH',
            'description': data[1]+"\n"+data[0]+"\n"+str(price)+data[5],
            'order_id': 'order_id_'+str(cls.count),
            'language': 'uk',
            'version': '3'
        }
        s = liqpay.cnb_signature(d)
        d = liqpay.cnb_data(d)
        r = requests.post('https://www.liqpay.ua/api/3/checkout/', data={
            'data': d,
            'signature': s})
        return r.url


#httpd = HTTPServer(('localhost', 8000), Response)
httpd = ThreadHTTPServer(('', int(os.environ.get('PORT', '3306'))), Response)
httpd.serve_forever()