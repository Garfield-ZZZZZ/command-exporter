import json
import os
import subprocess

from http.server import BaseHTTPRequestHandler, HTTPServer

class MetricHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		metricName = "script_result"
		try:
			metricName = os.environ['METRIC_NAME']
		except:
			print("METRIC_NAME is not a valid number, use default " + metricName)
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
				self.wfile.write(bytes(metricName + "{name=" + name + "} " + str(succeeded) + "\n", "utf8"))
		print("request completed")
		return

# Run the server
if __name__ == "__main__":
	port = 8080
	try:
		port = int(os.environ['PORT'])
	except:
		print("PORT is not a valid number, use default 8080")

	server = HTTPServer(('', port), MetricHandler)
	print('Starting http server on port ' + str(port) + '...')
	server.serve_forever()
