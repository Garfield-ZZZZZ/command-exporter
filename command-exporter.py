# the script starts a HTTP server on 8080, and wait for requests
# on start up, it reads the config.json file for all <name, command> pairs
# when a request comes, it executes each command, and return a line with the format of script_result{name=xxx, result=xxx}

import json
import os
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
				result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				returnCode = result.returncode
				print("Result: " + str(returnCode))
				succeeded = 1 if returnCode == 0 else 0
				self.wfile.write(bytes("script_result{name=" + name + "} " + str(succeeded) + "\n", "utf8"))
		print("request completed")
		return

# Run the server
if __name__ == "__main__":
	# check the "PORT" env var, assign it to port if it's a valid number, otherwise use 8080
	port = 8080
	try:
		port = int(os.environ['PORT'])
	except:
		print("PORT is not a valid number, use default 8080")

	server = HTTPServer(('', port), MetricHandler)
	print('Starting http server on port ' + str(port) + '...')
	server.serve_forever()
