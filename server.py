from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import requests


class CustomHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/main.html'

        if self.path.startswith('/api/'):
            number = self.path.split('/')[-1]

            facts = self.fetch_facts(number)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<p>'.join(facts).encode('utf-8'))

        else:
            try:
                with open(os.getcwd() + self.path, 'rb') as file:
                    content_type = self.guess_type(self.path)
                    self.send_response(200)
                    self.send_header('Content-type', content_type)
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)

    def fetch_facts(self, number):
        arr = []

        for i in range(20):
            api_url = f'http://numbersapi.com/{number}'
            response = requests.get(api_url)

            if response.ok:
                fact = response.text

                if fact not in arr and len(arr) < 5:
                    arr.append(fact)

                if len(arr) == 5 or i == 19:
                    break
            else:
                arr.append('Помилка: Internal Server Error')
                break

        return arr


def run(server_class=HTTPServer, handler_class=CustomHandler, port=8000):
    server_address = ('', port)
    with server_class(server_address, handler_class) as httpd:
        print(f"Starting server on port {port}")
        httpd.serve_forever()


if __name__ == '__main__':
    run()
