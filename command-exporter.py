# the script starts a HTTP server on 8080, and wait for requests
# on start up, it reads the config.json file for all <name, command> pairs
# when a request comes, it executes each command, and return a line with the format of script_result{name=xxx, result=xxx}

import json
import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer

class MetricHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()

		# Read config.json
		with open('config.json') as json_file:
			data = json.load(json_file)
			for p in data:
				name=p['name']
				command=p['command']
				print("Executing " + name + " with command: " + " ".join(command))
				result = subprocess.run(command, stdout=subprocess.PIPE)
				returnCode = result.returncode
				print("Result: " + str(returnCode))
				succeeded = 1 if returnCode == 0 else 0
				self.wfile.write(bytes("script_result{name=" + name + "} " + str(succeeded) + "\n", "utf8"))
		print("request completed")
		return

# Run the server
if __name__ == "__main__":
	server = HTTPServer(('', 8080), MetricHandler)
	print('Starting http server...')
	server.serve_forever()
