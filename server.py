# -*- coding: utf-8 -*-
from http.server import SimpleHTTPRequestHandler, HTTPServer
import requests
import os
import sys
import json

try:
    port_ = int(sys.argv[1]) if ((len(sys.argv) > 1) and (int(sys.argv[1]) < 65535) and (int(sys.argv[1]) > 0)) else 8000
except:
    print('Неправильний порт')
    port_ = 8000

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/main.html'

        if self.path.startswith('/api/'):
            city = self.path.split('/')[-1]

            details = self.fetch_(city)

            if details == 'Помилка: Internal Server Error':
                self.send_error(500, 'Помилка: Internal Server Error')
            elif details == 'Помилка: Інформація відсутня':
                self.send_response(404)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(details, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(details, ensure_ascii=False).encode('utf-8'))
        else:
            try:
                with open(os.getcwd() + self.path, 'rb') as file:
                    content_type = self.guess_type(self.path)
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, f'File Not Found: {self.path}')

    def fetch_(self, city):
        api_url = f'https://nominatim.openstreetmap.org/search.php?format=jsonv2&city={city}'
        
        try:
            response = requests.get(api_url, headers={'User-Agent': 'Students lab4'})
            response.raise_for_status()  
            if response.json():
                return response.json()
            else:
                return 'Помилка: Інформація відсутня'
        except:
            return 'Помилка: Internal Server Error'


def run(server_class=HTTPServer, handler_class=CustomHandler, port=port_):
    server_address = ('', port)
    with server_class(server_address, handler_class) as httpd:
        print(f"Starting server on port {port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
