import json
import http.server
import socketserver
from typing import Tuple
from http import HTTPStatus
import simplejson
from utilities import *


class Handler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    @property
    def service_up_response(self):
        return json.dumps({
                              "message": "Service is up. Please call /analyze with your text file with or without your filtering option."}).encode()

    @property
    def service_error(self):
        return json.dumps({"message": "Wrong parameter, error is occured!..."}).encode()

    def do_GET(self):
        if self.path == '/':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(self.service_up_response))

        if self.path == '/analyze':

            # get the info from rest api
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = simplejson.loads(self.data_string)

            if 'text' not in data.keys():
                self.send_response(HTTPStatus.NOT_ACCEPTABLE)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(self.service_error))
            else:
                # txt yi yukledigin yer burasi
                text = data['text']
                filter = []

                if 'analysis' in data.keys():
                    filter = data['analysis']

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                # filtreleri tek tek uygulama
                total_response = {}
                if len(filter) == 0:
                    # tum islemleri yap
                    words = text.split()

                    wc = wordCount(words)
                    total_response["wordCount"] = wc

                    mwl = medianWordLength(medianWord(wordCount(words), words))
                    total_response["medianWordLength"] = mwl

                    n_letter = letters(words)
                    total_response["letters"] = n_letter

                    ln = longest(words)
                    total_response["longest"] = ln

                    avg = avgLength(wordCount(words), letters(words))
                    total_response["avgLength"] = avg

                    dr = duration(words)
                    total_response["duration"] = dr

                    mw = medianWord(wordCount(words), words)
                    total_response["medianWord"] = mw

                    lng = guess_language(words)
                    total_response["language"] = lng

                    cw = most_common_words(words)
                    total_response["commonWords"] = cw
                else:
                    words = text.split()
                    for i in range(len(filter)):
                        if filter[i] == "wordCount":
                            wc = wordCount(words)
                            total_response["wordCount"] = wc

                        if filter[i] == "medianWordLength":
                            mwl = medianWordLength(medianWord(wordCount(words), words))
                            total_response["medianWordLength"] = mwl

                        if filter[i] == "letters":
                            n_letter = letters(words)
                            total_response["letters"] = n_letter

                        if filter[i] == "longest":
                            ln = longest(words)
                            total_response["longest"] = ln

                        if filter[i] == "avgLength":
                            avg = avgLength(wordCount(words), letters(words))
                            total_response["avgLength"] = avg

                        if filter[i] == "duration":
                            dr = duration(words)
                            total_response["duration"] = dr

                        if filter[i] == "medianWord":
                            mw = medianWord(wordCount(words), words)
                            total_response["medianWord"] = mw

                        if filter[i] == "language":
                            lng = guess_language(words)
                            total_response["language"] = lng

                        if filter[i] == "commonWords":
                            cw = most_common_words(words)
                            total_response["commonWords"] = cw

                # simdi response donus
                return self.wfile.write(bytes(json.dumps(total_response).encode()))


if __name__ == "__main__":
    PORT = 8080
    # Create an object of the above class
    my_server = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
    # Star the server
    print(f"Server started at {PORT}")
    my_server.serve_forever()