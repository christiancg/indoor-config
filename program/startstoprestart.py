import subprocess


class StartStopRestart:	
	OK = "ok"
	BAD_REQUEST = "bad_request"
	ERROR = "error"

	def process(self, todo):
		if todo == 1:
			return self._startServer()
		elif todo == 2:
			return self._stopServer()
		elif todo == 3:
			return self._restartServer()
		elif todo == 4:
			return self._hardRestartServer()
		else:
			return self.BAD_REQUEST 

	def _startServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'start'])
		return self.OK
		
	def _stopServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'stop'])
		return self.OK
		
	def _restartServer(self):
		subprocess.call(['sudo', 'service', 'indoor', 'restart'])
		return self.OK
		
	def _hardRestartServer(self):
		subprocess.call(['sudo', 'reboot'])
		return self.OK
